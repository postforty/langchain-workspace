import pytest
from unittest.mock import MagicMock
from domain.models import IncorrectAnswer
from use_cases.note_manager import NoteManagerUseCase

def test_note_manager_use_case():
    mock_repo = MagicMock()
    
    note = IncorrectAnswer(
        question_text="Q", 
        options=["1","2","3","4"], 
        user_answer_index=1, 
        correct_answer_index=0, 
        explanation="E"
    )
    
    mock_repo.get_all_incorrect_answers.return_value = [note]
    
    use_case = NoteManagerUseCase(note_repo=mock_repo)
    
    # 오답노트 저장
    use_case.save_note(note)
    mock_repo.save_incorrect_answer.assert_called_once_with(note)
    
    # 오답노트 조회
    notes = use_case.get_all_notes()
    assert len(notes) == 1
    assert notes[0] == note
