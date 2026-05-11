from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.core.interfaces import IVectorDB
from src.core.logger import get_logger

logger = get_logger(__name__)

class ChromaDBProvider(IVectorDB):
    """Concrete implementation of IVectorDB using Chroma."""
    
    def __init__(self, persist_directory: str = "src/data/chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self._vectorstore = None
        
    def _get_or_create_store(self):
        if self._vectorstore is None:
            # Load existing if available
            self._vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        return self._vectorstore

    def populate(self, documents: list) -> None:
        logger.info(f"Persisting {len(documents)} documents to ChromaDB at {self.persist_directory}")
        self._vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )

    def get_retriever(self, k: int = 2):
        logger.info(f"Creating retriever with k={k}")
        store = self._get_or_create_store()
        return store.as_retriever(search_kwargs={"k": k})
