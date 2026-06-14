import pytest
from unittest.mock import MagicMock
from domain.models import DocumentChunk, Question

# Red 단계: 구현체가 없어서 ImportError 발생
from use_cases.question_generator import QuestionGeneratorUseCase

def test_question_generator_use_case():
    mock_doc_repo = MagicMock()
    mock_llm_service = MagicMock()
    
    # 1. 랜덤 청크 반환 Mocking
    mock_doc_repo.get_random_chunks.return_value = [
        DocumentChunk(text="Chunk 1", metadata={}),
        DocumentChunk(text="Chunk 2", metadata={})
    ]
    
    # 2. LLM 출제 결과 Mocking
    mock_question = Question(question="Q", options=["1", "2", "3", "4"], answer_index=0, explanation="E")
    mock_llm_service.generate_question_from_context.return_value = mock_question
    
    # 유스케이스 조립 (의존성 주입)
    use_case = QuestionGeneratorUseCase(doc_repo=mock_doc_repo, llm_service=mock_llm_service)
    
    # 실행
    result = use_case.execute(chunk_count=2)
    
    # 검증
    assert result == mock_question
    mock_doc_repo.get_random_chunks.assert_called_once_with(count=2)
    mock_llm_service.generate_question_from_context.assert_called_once_with("Chunk 1\n\nChunk 2")
