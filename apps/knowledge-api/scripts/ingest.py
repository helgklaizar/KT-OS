import os
from pathlib import Path
import sys

# Add the parent directory to the Python path to import backend modules
sys.path.append(str(Path(__file__).parent.parent))

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from backend.core.llm import get_llm_and_embeddings

QDRANT_PATH = str(Path(__file__).parent.parent / "qdrant_storage")
COLLECTION_NAME = "knowledge_mesh_core"

def ingest_docs(docs_dir: str):
    print(f"Loading documents from {docs_dir}...")
    # We load markdown files as text
    loader = DirectoryLoader(docs_dir, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    if not documents:
        print(f"No documents found in {docs_dir}!")
        return

    print(f"Loaded {len(documents)} documents. Splitting...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    
    print(f"Created {len(docs)} chunks. Initializing Qdrant and Embeddings...")
    _, embeddings = get_llm_and_embeddings()
    
    client = QdrantClient(path=QDRANT_PATH)
    
    # Try to create collection if it doesn't exist
    try:
        client.get_collection(COLLECTION_NAME)
    except Exception:
        print(f"Creating collection {COLLECTION_NAME}...")
        test_embed = embeddings.embed_query("test")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=len(test_embed), distance=Distance.COSINE),
        )
    
    print("Ingesting chunks into Qdrant vector database...")
    Qdrant.from_documents(
        docs,
        embeddings,
        path=QDRANT_PATH,
        collection_name=COLLECTION_NAME,
    )
    
    print("Ingestion complete for", docs_dir)

if __name__ == "__main__":
    # Ingest the local .gemini and docs folders of the Know-Task-OS monorepo
    monorepo_root = Path(__file__).parent.parent.parent.parent
    
    target_dirs = [
        str(monorepo_root / ".gemini"),
        str(monorepo_root / "docs")
    ]
    
    for d in target_dirs:
        if os.path.exists(d):
            ingest_docs(d)
        else:
            print(f"Directory {d} does not exist, skipping.")
