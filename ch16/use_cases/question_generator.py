from typing import Optional
from domain.models import Question
from use_cases.interfaces import IDocumentRepository, IQuestionGenerator

class QuestionGeneratorUseCase:
    """PDF 문서 기반 4지선다 문제 출제 비즈니스 흐름 제어"""
    
    def __init__(self, doc_repo: IDocumentRepository, llm_service: IQuestionGenerator):
        self.doc_repo = doc_repo
        self.llm_service = llm_service
        
    def execute(self, chunk_count: int = 2) -> Optional[Question]:
        # 1. 저장소에서 랜덤 청크 추출
        chunks = self.doc_repo.get_random_chunks(count=chunk_count)
        if not chunks:
            return None
            
        # 2. 청크 텍스트 병합 (컨텍스트 구성)
        context = "\n\n".join(chunk.text for chunk in chunks)
        
        # 3. LLM을 통해 문제 출제
        question = self.llm_service.generate_question_from_context(context)
        return question
