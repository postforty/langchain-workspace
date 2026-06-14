from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class DocumentChunk(BaseModel):
    """PDF 문서에서 추출된 하나의 텍스트 조각을 나타내는 도메인 모델"""
    text: str
    metadata: dict = Field(default_factory=dict)
    
class Question(BaseModel):
    """AI가 출제한 4지선다 문제를 나타내는 도메인 모델"""
    question: str = Field(description="문제의 질문 내용")
    options: List[str] = Field(description="4개의 보기 리스트")
    answer_index: int = Field(description="정답 보기의 인덱스 (0부터 시작)")
    explanation: str = Field(description="문제에 대한 해설 및 풀이")

class IncorrectAnswer(BaseModel):
    """사용자가 틀린 문제(오답 노트)를 나타내는 도메인 모델"""
    id: Optional[int] = None
    question_text: str
    options: List[str]
    user_answer_index: int
    correct_answer_index: int
    explanation: str
    created_at: datetime = Field(default_factory=datetime.now)
