from src.core.interfaces import ILLMProvider, IVectorDB
from src.core.logger import get_logger
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = get_logger(__name__)

class SupportRAGUseCase:
    """Enterprise RAG Use Case (Framework-Agnostic Core Logic)."""
    
    def __init__(self, llm_provider: ILLMProvider, vector_db: IVectorDB):
        self.llm_provider = llm_provider
        self.vector_db = vector_db

    def index_documents(self, data_dir: str = "src/data/kb"):
        """Loads and chunks documents into the vector store."""
        logger.info(f"Loading documents from {data_dir}")
        loader = DirectoryLoader(data_dir, glob="*.md", loader_cls=TextLoader)
        docs = loader.load()

        logger.info(f"Splitting {len(docs)} documents.")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(docs)
        
        self.vector_db.populate(chunks)
        logger.info("Documents successfully indexed.")

    def answer_query(self, query: str) -> str:
        """Process a query through the RAG pipeline."""
        logger.info(f"Received query: {query}")
        
        # 1. Retrieve
        retriever = self.vector_db.get_retriever(k=2)
        docs = retriever.invoke(query)
        context = "\n".join([doc.page_content for doc in docs])
        
        # 2. Format Prompt
        prompt = f"""<|system|>
You are a polite corporate support assistant. Use the following context to answer the user's question. If you don't know the answer based on the context, say so. Do not invent information.
Context: {context}</s>
<|user|>
{query}</s>
<|assistant|>"""
        
        # 3. Generate
        llm = self.llm_provider.get_llm()
        # The HuggingFace pipeline returns a list of dicts or just text depending on the wrapper
        response = llm.invoke(prompt)
        
        logger.info("Response generated successfully.")
        return response
