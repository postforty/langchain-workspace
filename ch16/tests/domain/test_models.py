from domain.models import DocumentChunk, Question, IncorrectAnswer
from datetime import datetime

def test_document_chunk_creation():
    chunk = DocumentChunk(text="test content", metadata={"page": 1})
    assert chunk.text == "test content"
    assert chunk.metadata == {"page": 1}

def test_question_creation():
    q = Question(
        question="What is 1+1?",
        options=["1", "2", "3", "4"],
        answer_index=1,
        explanation="1+1=2"
    )
    assert q.question == "What is 1+1?"
    assert q.options == ["1", "2", "3", "4"]
    assert q.answer_index == 1

def test_incorrect_answer_creation():
    note = IncorrectAnswer(
        question_text="What is 1+1?",
        options=["1", "2", "3", "4"],
        user_answer_index=0,
        correct_answer_index=1,
        explanation="1+1=2"
    )
    assert note.id is None
    assert isinstance(note.created_at, datetime)
