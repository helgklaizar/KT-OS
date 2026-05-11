import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from catboost import CatBoostClassifier
import re

# Initialize FastAPI app
app = FastAPI(
    title="Support Assistant Routing API",
    description="API for routing support tickets to the correct department using Machine Learning.",
    version="1.0.0"
)

# Global variables for models
vectorizer = None
model = None

# Path configurations
MODEL_DIR = os.path.join(os.path.dirname(__file__), '../models/saved')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
MODEL_PATH = os.path.join(MODEL_DIR, 'catboost_classifier.cbm')

class TicketRequest(BaseModel):
    text: str

class TicketResponse(BaseModel):
    department: str
    confidence: float

def clean_text(text: str) -> str:
    # Same cleaning function used during training
    text = re.sub(r'[^\w\s\!\?]', '', text)
    return text.lower().strip()

@app.on_event("startup")
def load_ml_models():
    """Load ML models on application startup."""
    global vectorizer, model
    try:
        print(f"Loading TF-IDF Vectorizer from {VECTORIZER_PATH}...")
        vectorizer = joblib.load(VECTORIZER_PATH)
        
        print(f"Loading CatBoost Model from {MODEL_PATH}...")
        model = CatBoostClassifier()
        model.load_model(MODEL_PATH)
        
        print("✅ Models loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading models: {e}")

@app.get("/")
def read_root():
    return {"status": "online", "model": "CatBoost TF-IDF Routing Engine"}

@app.post("/predict", response_model=TicketResponse)
def predict_department(ticket: TicketRequest):
    """Predict the department for a given support ticket."""
    if not vectorizer or not model:
        return {"error": "Models not loaded. Check server logs."}
        
    # 1. Clean the incoming text
    cleaned_text = clean_text(ticket.text)
    
    # 2. Vectorize the text
    X_vec = vectorizer.transform([cleaned_text])
    
    # 3. Predict using CatBoost
    prediction = model.predict(X_vec)
    predicted_class = prediction[0][0]
    
    # 4. Get confidence (probability)
    probabilities = model.predict_proba(X_vec)[0]
    confidence = float(max(probabilities))
    
    return TicketResponse(
        department=predicted_class,
        confidence=confidence
    )
