import streamlit as st
from domain.models import IncorrectAnswer
from use_cases.question_generator import QuestionGeneratorUseCase
from use_cases.qa_bot import QABotUseCase
from use_cases.note_manager import NoteManagerUseCase
from interface_adapters.document_parser.pdf_parser import PDFParser

def render_ui(
    pdf_parser: PDFParser,
    doc_repo,  # IDocumentRepository
    question_generator: QuestionGeneratorUseCase,
    qa_bot: QABotUseCase,
    note_manager: NoteManagerUseCase
):
    st.set_page_config(page_title="AI 학습 도우미", page_icon="🤖", layout="wide")
    st.title("🤖 AI 학습 도우미 챗봇")
    st.markdown("PDF 교재를 업로드하고, AI와 함께 문제를 풀거나 질의응답을 진행해 보세요. (Clean Architecture 기반)")

    # 세션 상태 초기화
    if "is_indexed" not in st.session_state:
        st.session_state.is_indexed = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = None

    with st.sidebar:
        st.header("설정 및 업로드")
        uploaded_file = st.file_uploader("PDF 교재 업로드", type=["pdf"])
        
        if uploaded_file and not st.session_state.is_indexed:
            with st.spinner("문서를 분석하고 인덱싱하는 중입니다... (FAISS + Ollama)"):
                # 파일 바이트 읽기
                file_bytes = uploaded_file.read()
                # 파싱 및 청크 분할 (방어 로직 1: Overlap 적용됨)
                chunks = pdf_parser.parse_and_chunk(file_bytes, uploaded_file.name)
                # 벡터 DB에 인덱싱
                doc_repo.index_documents(chunks)
                st.session_state.is_indexed = True
                st.success("문서 파싱 및 인덱싱 완료!")
                
        st.divider()
        st.subheader("모드 선택")
        mode = st.radio("학습 모드를 선택하세요", ("문제 풀기", "오답 노트", "질의응답 (Q&A)"))

    if not st.session_state.is_indexed:
        st.warning("👈 왼쪽 사이드바에서 PDF 교재를 먼저 업로드해 주세요.")
        return

    if mode == "문제 풀기":
        st.subheader("📝 4지선다 문제 풀이")
        
        if st.button("새로운 문제 출제 (랜덤)"):
            with st.spinner("AI가 문맥을 분석하여 문제를 출제하고 있습니다..."):
                q = question_generator.execute()
                if q:
                    st.session_state.current_question = q
                else:
                    st.error("문제 출제에 실패했습니다. 다시 시도해주세요.")
                    
        q = st.session_state.current_question
        if q:
            st.write(f"**문제:** {q.question}")
            
            with st.form("question_form"):
                user_choice = st.radio("정답을 선택하세요:", q.options, index=None)
                submitted = st.form_submit_button("정답 확인")
                
                if submitted:
                    if user_choice is None:
                        st.warning("보기를 선택해주세요!")
                    else:
                        user_index = q.options.index(user_choice)
                        if user_index == q.answer_index:
                            st.success("정답입니다! 🎉")
                            st.info(f"**해설:** {q.explanation}")
                        else:
                            st.error(f"오답입니다. 정답은 {q.options[q.answer_index]} 입니다.")
                            st.info(f"**해설:** {q.explanation}")
                            
                            # 오답 노트에 저장
                            note = IncorrectAnswer(
                                question_text=q.question,
                                options=q.options,
                                user_answer_index=user_index,
                                correct_answer_index=q.answer_index,
                                explanation=q.explanation
                            )
                            note_manager.save_note(note)
                            st.toast("오답 노트에 저장되었습니다.")

    elif mode == "오답 노트":
        st.subheader("📓 오답 노트")
        notes = note_manager.get_all_notes()
        if not notes:
            st.info("아직 저장된 오답이 없습니다.")
        else:
            for note in notes:
                with st.expander(f"[{note.created_at.strftime('%Y-%m-%d %H:%M')}] {note.question_text}"):
                    st.write(f"**내 선택:** {note.options[note.user_answer_index]}")
                    st.write(f"**정답:** {note.options[note.correct_answer_index]}")
                    st.write(f"**해설:** {note.explanation}")

    elif mode == "질의응답 (Q&A)":
        st.subheader("💬 실시간 질의응답 (RAG)")
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        user_query = st.chat_input("교재 내용에 대해 질문하세요.")
        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)
                
            with st.chat_message("assistant"):
                with st.spinner("답변을 생성 중입니다..."):
                    answer = qa_bot.execute(user_query)
                    st.write(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
