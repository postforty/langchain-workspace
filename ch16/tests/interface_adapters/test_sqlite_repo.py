import pytest
from domain.models import IncorrectAnswer
from interface_adapters.repositories.sqlite_repo import SQLiteIncorrectNoteRepository

@pytest.fixture
def repo(tmp_path):
    # tmp_path is a built-in pytest fixture that provides a temporary directory unique to the test invocation
    db_path = tmp_path / "test_notes.db"
    return SQLiteIncorrectNoteRepository(db_path=str(db_path))

def test_save_and_get_incorrect_answer(repo):
    note = IncorrectAnswer(
        question_text="What is AI?",
        options=["A", "B", "C", "D"],
        user_answer_index=1,
        correct_answer_index=0,
        explanation="AI is Artificial Intelligence"
    )
    
    repo.save_incorrect_answer(note)
    
    notes = repo.get_all_incorrect_answers()
    
    assert len(notes) == 1
    assert notes[0].question_text == "What is AI?"
    assert notes[0].options == ["A", "B", "C", "D"]
    assert notes[0].user_answer_index == 1
    assert notes[0].correct_answer_index == 0
    assert notes[0].explanation == "AI is Artificial Intelligence"
    assert notes[0].id is not None  # ID should be auto-incremented and assigned
