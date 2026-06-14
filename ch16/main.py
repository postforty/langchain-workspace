import streamlit as st
import os

# 환경 변수 로드 (.env가 있는 경우)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from interface_adapters.document_parser.pdf_parser import PDFParser
from interface_adapters.repositories.sqlite_repo import SQLiteIncorrectNoteRepository
from interface_adapters.repositories.faiss_repo import FAISSRepository
from interface_adapters.llm_services.langchain_client import LangChainGeminiClient

from use_cases.question_generator import QuestionGeneratorUseCase
from use_cases.qa_bot import QABotUseCase
from use_cases.note_manager import NoteManagerUseCase

from presentation.streamlit_app import render_ui

# DI (의존성 주입) 설정 함수: Streamlit 세션 간 재사용을 위해 캐싱
@st.cache_resource
def setup_di_container():
    """모든 어댑터와 유스케이스를 인스턴스화하고 의존성을 조립합니다."""
    # Cache invalidation trigger (코드 수정 사항 반영을 위함)
    # 1. 인터페이스 어댑터(구현체) 인스턴스화
    pdf_parser = PDFParser()
    sqlite_repo = SQLiteIncorrectNoteRepository("incorrect_notes.db")
    faiss_repo = FAISSRepository(model_name="bge-m3")
    llm_client = LangChainGeminiClient(model_name="gemini-3.1-flash-lite")
    
    # 2. 유스케이스 조립 (어댑터 주입)
    question_generator = QuestionGeneratorUseCase(doc_repo=faiss_repo, llm_service=llm_client)
    qa_bot = QABotUseCase(doc_repo=faiss_repo, qa_service=llm_client)
    note_manager = NoteManagerUseCase(note_repo=sqlite_repo)
    
    return pdf_parser, faiss_repo, question_generator, qa_bot, note_manager

def main():
    # 1. 의존성 컨테이너에서 객체 가져오기
    pdf_parser, faiss_repo, question_generator, qa_bot, note_manager = setup_di_container()
    
    # 2. 뷰 계층으로 제어권 위임 (객체 주입)
    render_ui(
        pdf_parser=pdf_parser,
        doc_repo=faiss_repo,
        question_generator=question_generator,
        qa_bot=qa_bot,
        note_manager=note_manager
    )

if __name__ == "__main__":
    main()
