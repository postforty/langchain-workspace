import sqlite3
import json
from typing import List
from domain.models import IncorrectAnswer
from use_cases.interfaces import IIncorrectNoteRepository
from datetime import datetime

class SQLiteIncorrectNoteRepository(IIncorrectNoteRepository):
    def __init__(self, db_path: str = "incorrect_notes.db"):
        self.db_path = db_path
        self._init_db()
        
    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS incorrect_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            options JSON NOT NULL,
            user_answer_index INTEGER NOT NULL,
            correct_answer_index INTEGER NOT NULL,
            explanation TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def save_incorrect_answer(self, note: IncorrectAnswer) -> None:
        query = """
        INSERT INTO incorrect_answers 
        (question_text, options, user_answer_index, correct_answer_index, explanation, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                note.question_text,
                json.dumps(note.options, ensure_ascii=False),
                note.user_answer_index,
                note.correct_answer_index,
                note.explanation,
                note.created_at.isoformat()
            ))
            conn.commit()
            
    def get_all_incorrect_answers(self) -> List[IncorrectAnswer]:
        query = "SELECT id, question_text, options, user_answer_index, correct_answer_index, explanation, created_at FROM incorrect_answers ORDER BY created_at DESC"
        results = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            for row in rows:
                note = IncorrectAnswer(
                    id=row[0],
                    question_text=row[1],
                    options=json.loads(row[2]),
                    user_answer_index=row[3],
                    correct_answer_index=row[4],
                    explanation=row[5],
                    created_at=datetime.fromisoformat(row[6])
                )
                results.append(note)
                
        return results
