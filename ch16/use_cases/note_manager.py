from typing import List
from domain.models import IncorrectAnswer
from use_cases.interfaces import IIncorrectNoteRepository

class NoteManagerUseCase:
    """오답 노트 저장 및 조회 비즈니스 흐름 제어"""
    
    def __init__(self, note_repo: IIncorrectNoteRepository):
        self.note_repo = note_repo
        
    def save_note(self, note: IncorrectAnswer) -> None:
        self.note_repo.save_incorrect_answer(note)
        
    def get_all_notes(self) -> List[IncorrectAnswer]:
        return self.note_repo.get_all_incorrect_answers()
