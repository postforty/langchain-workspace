# AI 학습 도우미 챗봇 작업 목록 (Clean Architecture & TDD)

## 1. 기반 구현 완료 항목
- [x] `domain/models.py`: 핵심 엔티티(Question, IncorrectAnswer 등) Pydantic 모델 정의
- [x] `use_cases/interfaces.py`: 외부 어댑터들이 구현해야 할 추상 인터페이스(Repository 등) 정의
- [x] `interface_adapters/document_parser/pdf_parser.py`: PyMuPDF 파싱 및 Chunking (방어 로직 1 구현)
- [x] `interface_adapters/repositories/sqlite_repo.py`: SQLite 기반 오답 노트 DB 처리 구현

## 2. TDD 환경 세팅 및 기존 코드 테스트 (신규)
- [x] `pytest`, `pytest-mock` 등 테스트 의존성 패키지 설치 및 환경 설정
- [x] `tests/domain/test_models.py`: 도메인 모델 검증 테스트 작성
- [x] `tests/interface_adapters/test_pdf_parser.py`: PDF 파싱 및 Chunk Overlap 로직 테스트 작성
- [x] `tests/interface_adapters/test_sqlite_repo.py`: 오답노트 DB CRUD 로직 테스트 작성 (Mock 또는 In-memory DB 활용)

## 3. FAISS 벡터 DB 구현 (TDD 방식)
- [x] [Red] `tests/interface_adapters/test_faiss_repo.py`: 임베딩 및 검색에 대한 실패하는 테스트 작성 (Mocking 활용)
- [x] [Green/Refactor] `interface_adapters/repositories/faiss_repo.py`: 테스트를 통과하는 실제 코드 구현 (방어 로직 2, 3)

## 4. LangChain & Gemini 통신 구현 (TDD 방식)
- [x] [Red] `tests/interface_adapters/test_langchain_client.py`: 문제 출제 및 RAG 프롬프트 제어 실패하는 테스트 작성
- [x] [Green/Refactor] `interface_adapters/llm_services/langchain_client.py`: 테스트를 통과하는 실제 코드 구현 (방어 로직 4)

## 5. Use Case 비즈니스 흐름 조립 (TDD 방식)
- [x] [Red] `tests/use_cases/`: 문제 생성, 질의응답, 오답노트 흐름 제어에 대한 단위 테스트 작성
- [x] [Green/Refactor] `use_cases/`: `question_generator.py`, `qa_bot.py`, `note_manager.py` 실제 비즈니스 흐름 구현

## 6. UI 및 앱 실행계층
- [x] `presentation/streamlit_app.py`: Streamlit UI 로직 이전 및 뷰 구성
- [x] `main.py`: 의존성 주입(DI) 컨테이너 구성 및 앱 진입점 작성
- [ ] 전체 E2E (End-to-End) 통합 테스트 및 버그 수정
