import pytest
from unittest.mock import MagicMock
from domain.models import Question

# This import will fail initially (Red phase)
from interface_adapters.llm_services.langchain_client import LangChainGeminiClient

def test_generate_question_from_context(mocker):
    # ChatGoogleGenerativeAI 클래스 Mocking
    mocker.patch("interface_adapters.llm_services.langchain_client.ChatGoogleGenerativeAI")
    
    client = LangChainGeminiClient()
    
    # 내부 _question_chain 모킹 (프롬프트+LLM 체인)
    mock_chain = mocker.MagicMock()
    mock_question = Question(
        question="What is AI?",
        options=["A", "B", "C", "D"],
        answer_index=0,
        explanation="AI is Artificial Intelligence."
    )
    mock_chain.invoke.return_value = mock_question
    client._question_chain = mock_chain
    
    context = "AI stands for Artificial Intelligence."
    result = client.generate_question_from_context(context)
    
    assert result is not None
    assert result.question == "What is AI?"
    assert len(result.options) == 4
    assert result.answer_index == 0
    # 체인이 context를 인자로 받아 호출되었는지 검증
    mock_chain.invoke.assert_called_once_with({"context": context})

def test_answer_question(mocker):
    mocker.patch("interface_adapters.llm_services.langchain_client.ChatGoogleGenerativeAI")
    
    client = LangChainGeminiClient()
    
    mock_chain = mocker.MagicMock()
    mock_chain.invoke.return_value = "AI stands for Artificial Intelligence."
    client._qa_chain = mock_chain
    
    query = "What is AI?"
    context = "AI stands for Artificial Intelligence."
    answer = client.answer_question(query, context)
    
    assert answer == "AI stands for Artificial Intelligence."
    # 체인이 query와 context를 인자로 받아 호출되었는지 검증 (방어 로직 4 확인)
    mock_chain.invoke.assert_called_once_with({"query": query, "context": context})
