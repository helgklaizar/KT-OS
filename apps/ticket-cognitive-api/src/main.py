from src.core.logger import get_logger
from src.services.local_llm import LocalTinyLlamaProvider
from src.services.chroma_db import ChromaDBProvider
from src.use_cases.rag_use_case import SupportRAGUseCase
from src.use_cases.agent_router import MultiAgentRouter

logger = get_logger(__name__)

def main():
    logger.info("Initializing Enterprise AI Supervisor...")
    
    # 1. Dependency Injection
    llm_provider = LocalTinyLlamaProvider()
    vector_db = ChromaDBProvider()
    
    # 2. RAG Use Case (Knowledge Base)
    rag_use_case = SupportRAGUseCase(llm_provider=llm_provider, vector_db=vector_db)
    # rag_use_case.index_documents() # Uncomment if you need to re-index
    
    # 3. Agent Supervisor (Decides: RAG vs SQL)
    supervisor = MultiAgentRouter(llm_provider=llm_provider, rag_use_case=rag_use_case)
    
    print("\n" + "="*50)
    print("🤖 AI Supervisor Online.")
    print("="*50 + "\n")
    
    # TEST 1: Policy Question -> Should trigger Knowledge Base RAG
    query1 = "Can you check the company policy on remote work?"
    print(f"\n[USER]: {query1}")
    answer1 = supervisor.run_query(query1)
    print(f"[AGENT]: {answer1}")
    
    # TEST 2: Database Question -> Should trigger SQLite Query
    query2 = "How many employees are in the Sales department?"
    print(f"\n[USER]: {query2}")
    answer2 = supervisor.run_query(query2)
    print(f"[AGENT]: {answer2}")

if __name__ == "__main__":
    main()
