from abc import ABC, abstractmethod
from typing import Any

class ILLMProvider(ABC):
    """Abstract interface for LLM Providers. Ensures we can swap Local/Cloud LLMs."""
    
    @abstractmethod
    def get_llm(self) -> Any:
        pass

class IVectorDB(ABC):
    """Abstract interface for Vector Stores."""
    
    @abstractmethod
    def get_retriever(self, k: int = 2) -> Any:
        pass
        
    @abstractmethod
    def populate(self, documents: list) -> None:
        pass
