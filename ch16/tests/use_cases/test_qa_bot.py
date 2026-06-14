import pytest
from unittest.mock import MagicMock
from domain.models import DocumentChunk
from use_cases.qa_bot import QABotUseCase

def test_qa_bot_use_case():
    mock_doc_repo = MagicMock()
    mock_qa_service = MagicMock()
    
    # 1. RAG 검색 결과 Mocking
    mock_doc_repo.search_similar.return_value = [
        DocumentChunk(text="Related text 1", metadata={}),
        DocumentChunk(text="Related text 2", metadata={})
    ]
    
    # 2. LLM 응답 Mocking
    mock_qa_service.answer_question.return_value = "Here is the answer."
    
    use_case = QABotUseCase(doc_repo=mock_doc_repo, qa_service=mock_qa_service)
    
    result = use_case.execute(query="What is this?")
    
    assert result == "Here is the answer."
    mock_doc_repo.search_similar.assert_called_once_with("What is this?", top_k=3)
    mock_qa_service.answer_question.assert_called_once_with("What is this?", "Related text 1\n\nRelated text 2")
