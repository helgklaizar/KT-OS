import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from src.core.interfaces import ILLMProvider
from src.core.logger import get_logger

logger = get_logger(__name__)

class LocalTinyLlamaProvider(ILLMProvider):
    """Concrete implementation of ILLMProvider using TinyLlama running locally."""
    
    def __init__(self, model_id: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.model_id = model_id
        self._llm = None
        
    def get_llm(self) -> HuggingFacePipeline:
        if self._llm is not None:
            return self._llm
            
        logger.info(f"Loading local LLM model: {self.model_id}")
        tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        
        # Use MPS on Mac if available, else CPU
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_id, 
            torch_dtype=torch.float32, 
            low_cpu_mem_usage=True
        ).to(device)

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=150,
            temperature=0.1,
            repetition_penalty=1.1,
            device_map=device
        )
        
        self._llm = HuggingFacePipeline(pipeline=pipe)
        return self._llm
