from pathlib import Path
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from backend.core.llm import get_llm_and_embeddings
import logging

QDRANT_PATH = str(Path(__file__).parent.parent.parent / "qdrant_storage")
COLLECTION_NAME = "knowledge_mesh_core"

class RAGService:
    def __init__(self):
        # 1. Connect to local storage
        self.client = QdrantClient(path=QDRANT_PATH)
        
        # Intelligent provider selection (Local-First: Ollama -> Fake)
        self.llm, self.embeddings = get_llm_and_embeddings()
        
        # 2. Initialize Vector Store
        self.vector_store = Qdrant(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embeddings=self.embeddings
        )
        
        # 3. Configure Retriever (search top-3 chunks)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        
        # 5. Build Prompt
        template = """You are an intelligent agent for the enterprise Knowledge Mesh.
Use the provided context to answer the user's question.
If the answer is not in the context, honestly state that you do not know (no hallucinations).
Answer in a structured, professional, and concise manner.

Context:
{context}

Question: {question}

Answer:"""
        self.prompt = ChatPromptTemplate.from_template(template)
        
        # 6. Assemble LangChain LCEL Pipeline
        self.chain = (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def _format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def ask(self, query: str) -> dict:
        # Get source documents (to return them as sources)
        docs = self.retriever.invoke(query)
        sources = [doc.metadata.get('source', 'Unknown') for doc in docs]
        
        # Generate answer
        answer = self.chain.invoke(query)
        
        # Remove duplicates from sources
        unique_sources = list(set(sources))
        
        return {
            "answer": answer,
            "sources": unique_sources
        }

    def search(self, query: str) -> list[dict]:
        # Returns raw documents without LLM processing (useful for Agent-BOS)
        docs = self.retriever.invoke(query)
        return [{"content": doc.page_content, "source": doc.metadata.get('source', 'Unknown')} for doc in docs]

# Singleton instance for reuse in FastAPI
rag_service = RAGService()
