from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mlx_lm import load, generate
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import os
import uuid

app = FastAPI(title="Aegis AI Brain", description="Local MLX-based engine + Qdrant RAG Memory")

MODEL_NAME = os.getenv("AEGIS_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
QDRANT_PATH = "qdrant_db"
COLLECTION_NAME = "aegis_feedback"

model = None
tokenizer = None
embedder = None
qdrant = None

class AnalysisRequest(BaseModel):
    rule_name: str
    file_path: str
    match_content: str

class AnalysisResponse(BaseModel):
    is_true_positive: bool
    reasoning: str

class FeedbackRequest(BaseModel):
    rule_name: str
    file_path: str
    match_content: str
    is_false_positive: bool

@app.on_event("startup")
async def startup_event():
    global model, tokenizer, embedder, qdrant
    print(f"Loading MLX model {MODEL_NAME}...")
    try:
        model, tokenizer = load(MODEL_NAME)
        print("MLX Model loaded successfully!")
    except Exception as e:
        print(f"Failed to load MLX model: {e}")

    print("Loading Embedder and Qdrant...")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    qdrant = QdrantClient(path=QDRANT_PATH)
    
    collections = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION_NAME not in collections:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
    print("Memory DB initialized.")

@app.post("/feedback")
async def add_feedback(req: FeedbackRequest):
    if not qdrant or not embedder:
        raise HTTPException(status_code=503, detail="Memory not initialized")
    
    vector = embedder.encode(req.match_content).tolist()
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={
            "rule_name": req.rule_name,
            "file_path": req.file_path,
            "match_content": req.match_content,
            "is_false_positive": req.is_false_positive
        }
    )
    qdrant.upsert(collection_name=COLLECTION_NAME, points=[point])
    return {"status": "ok", "message": "Feedback saved to memory"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_finding(req: AnalysisRequest):
    if model is None or embedder is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # 1. Check Qdrant Memory First
    vector = embedder.encode(req.match_content).tolist()
    search_result = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=1,
        score_threshold=0.95
    )
    
    if search_result:
        closest = search_result[0]
        if closest.payload.get("is_false_positive") == True:
            return AnalysisResponse(
                is_true_positive=False,
                reasoning="Suppressed by RAG Memory (previously marked as False Positive)."
            )

    # 2. Fallback to LLM
    prompt = f"""<|im_start|>system
You are a strict security auditor. Your task is to analyze a matched code snippet and determine if it is a REAL security vulnerability (True Positive) or a safe, test/dummy value (False Positive).
Reply ONLY with a JSON object in this exact format: {{"is_true_positive": true/false, "reasoning": "short explanation"}}
<|im_end|>
<|im_start|>user
Rule Triggered: {req.rule_name}
File Path: {req.file_path}
Matched Content: {req.match_content}

Is this a real security risk or just a dummy/test value?
<|im_end|>
<|im_start|>assistant
"""
    try:
        response = generate(model, tokenizer, prompt=prompt, max_tokens=100, verbose=False)
        response_lower = response.lower()
        is_tp = "true" in response_lower and "false" not in response_lower
        
        if "true" in response_lower and "false" in response_lower:
            is_tp = response_lower.find("true") < response_lower.find("false")

        return AnalysisResponse(
            is_true_positive=is_tp,
            reasoning=response.strip()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
