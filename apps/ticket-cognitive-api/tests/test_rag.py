import pytest
import os
import shutil
from src.services.chroma_db import ChromaDBProvider
from src.services.local_llm import LocalTinyLlamaProvider
from src.use_cases.rag_use_case import SupportRAGUseCase

@pytest.fixture(scope="module")
def real_rag_system():
    """Integration Test Fixture: Uses REAL PyTorch embeddings, REAL ChromaDB, and REAL LLM."""
    test_db_dir = "src/data/chroma_db_real_test"
    
    # 1. Real Vector DB Provider
    vector_db = ChromaDBProvider(persist_directory=test_db_dir)
    
    # 2. Real LLM Provider (will download/load TinyLlama into memory)
    llm_provider = LocalTinyLlamaProvider()
    
    # 3. Use Case
    use_case = SupportRAGUseCase(llm_provider=llm_provider, vector_db=vector_db)
    
    # Pre-index actual files from our fake DB
    use_case.index_documents(data_dir="src/data/kb")
    
    yield use_case
    
    # Teardown
    if os.path.exists(test_db_dir):
        shutil.rmtree(test_db_dir)

def test_real_retrieval_and_generation(real_rag_system):
    """End-to-End Test: Queries the real LLM with a RAG prompt."""
    query = "How many days do I have to return an item?"
    
    # This will trigger the actual HuggingFace Pipeline + PyTorch Vector Search
    answer = real_rag_system.answer_query(query)
    
    # The LLM output might vary slightly, but it should contain "14" or "days"
    assert answer is not None
    assert type(answer) == str
    assert len(answer) > 10, "Response should be a meaningful sentence"
    print(f"\nREAL LLM RESPONSE: {answer}")
