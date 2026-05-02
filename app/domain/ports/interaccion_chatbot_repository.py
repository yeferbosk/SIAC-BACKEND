from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.interaccion_chatbot import InteraccionChatbot

class InteraccionChatbotRepository(ABC):
    @abstractmethod
    def save(self, interaccion: InteraccionChatbot) -> InteraccionChatbot:
        pass

    @abstractmethod
    def get_by_id(self, interaccion_id: int) -> Optional[InteraccionChatbot]:
        pass

    @abstractmethod
    def get_all() -> List[InteraccionChatbot]:
        pass
