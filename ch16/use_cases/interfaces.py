from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models import DocumentChunk, Question, IncorrectAnswer

class IDocumentRepository(ABC):
    """문서 임베딩 및 벡터 검색을 담당하는 저장소 인터페이스 (Vector DB)"""
    
    @abstractmethod
    def index_documents(self, chunks: List[DocumentChunk]) -> None:
        pass
        
    @abstractmethod
    def search_similar(self, query: str, top_k: int = 3) -> List[DocumentChunk]:
        pass

    @abstractmethod
    def get_random_chunks(self, count: int = 1) -> List[DocumentChunk]:
        pass


class IIncorrectNoteRepository(ABC):
    """오답 노트를 데이터베이스에 저장/조회하는 인터페이스 (SQLite 등)"""
    
    @abstractmethod
    def save_incorrect_answer(self, note: IncorrectAnswer) -> None:
        pass
        
    @abstractmethod
    def get_all_incorrect_answers(self) -> List[IncorrectAnswer]:
        pass


class IQuestionGenerator(ABC):
    """LLM을 이용하여 4지선다 문제를 출제하는 인터페이스"""
    
    @abstractmethod
    def generate_question_from_context(self, context: str) -> Optional[Question]:
        """제공된 컨텍스트(문맥)를 바탕으로 문제를 생성 (정보 부족 시 None 반환)"""
        pass


class IQAService(ABC):
    """LLM을 이용하여 질의응답을 수행하는 인터페이스"""
    
    @abstractmethod
    def answer_question(self, query: str, context: str) -> str:
        """제공된 컨텍스트(문맥)를 바탕으로 사용자 질문에 답변"""
        pass
