from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.logger import get_logger
from src.services.local_llm import LocalTinyLlamaProvider
from src.services.chroma_db import ChromaDBProvider
from src.use_cases.rag_use_case import SupportRAGUseCase
from src.use_cases.agent_router import MultiAgentRouter
import uvicorn

logger = get_logger(__name__)

app = FastAPI(
    title="CAIO Agentic Supervisor API",
    description="Enterprise API wrapping RAG and SQL Agent Routing.",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    status: str
    response: str

# Singleton instances for the app lifecycle
llm_provider = None
vector_db = None
rag_use_case = None
supervisor = None

@app.on_event("startup")
def startup_event():
    global llm_provider, vector_db, rag_use_case, supervisor
    logger.info("Starting up FastAPI and Loading ML Models...")
    try:
        llm_provider = LocalTinyLlamaProvider()
        vector_db = ChromaDBProvider()
        
        # We assume data is already indexed via init script
        rag_use_case = SupportRAGUseCase(llm_provider=llm_provider, vector_db=vector_db)
        supervisor = MultiAgentRouter(llm_provider=llm_provider, rag_use_case=rag_use_case)
        
        # Pre-heat the agent logic
        supervisor.initialize_agent()
        logger.info("System Ready to receive requests.")
    except Exception as e:
        logger.error(f"Failed during startup: {str(e)}")

@app.post("/ask", response_model=QueryResponse)
def ask_agent(query: QueryRequest):
    """Ask the Agent a question. It will route to SQL or RAG automatically."""
    if not supervisor:
        raise HTTPException(status_code=503, detail="Model is still loading. Please try again later.")
        
    try:
        answer = supervisor.run_query(query.text)
        return QueryResponse(status="success", response=answer)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
