from abc import ABC, abstractmethod
from typing import List, Any

class BaseLLM(ABC):
    @abstractmethod
    def connect(self, connection_info: Any):
        pass

    @abstractmethod
    def summarize(self, user_query: str, documents: List[str]) -> str:
        pass
