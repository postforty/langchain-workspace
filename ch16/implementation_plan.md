# AI 학습 도우미 챗봇 시스템 설계 및 구현 계획

이 계획서는 PDF 문서를 기반으로 4지선다 문제를 출제하고, 오답 노트를 관리하며, 실시간 질의응답이 가능한 AI 학습 도우미 챗봇을 **클린 아키텍처(Clean Architecture)** 기반으로 개발하기 위한 아키텍처를 정의합니다.

## 1. 개요 및 확정된 기술 스택
- **프레임워크**: LangChain
- **UI/UX**: Streamlit
- **LLM (텍스트 생성)**: Google Gemini (`gemini-3.1-flash-lite`)
- **임베딩 모델**: Ollama (`bge-m3`)
- **Vector DB**: FAISS
- **문서 파싱**: PyMuPDF
- **데이터베이스**: SQLite3 (Python 내장)

---

## 2. 클린 아키텍처 (Clean Architecture) 설계

유지보수성과 확장성, 테스트 용이성을 극대화하기 위해 비즈니스 로직과 외부 프레임워크(UI, DB, LLM)를 분리하는 클린 아키텍처 패턴을 도입합니다. 프로젝트 구조는 다음과 같이 나뉩니다.

### 2.1 디렉토리 및 계층(Layer) 구조

```text
ch16/
├── domain/                  # [엔티티] 핵심 비즈니스 규칙
│   └── models.py            # Question, IncorrectAnswer, DocumentChunk 데이터 모델
├── use_cases/               # [유스케이스] 애플리케이션 서비스 로직
│   ├── question_generator.py# 문제 출제 흐름 제어
│   ├── qa_bot.py            # RAG 질의응답 흐름 제어
│   └── note_manager.py      # 오답 노트 저장 및 조회 흐름 제어
├── interface_adapters/      # [어댑터] 외부 인터페이스와 도메인을 연결
│   ├── repositories/        # DB 접근 및 저장소
│   │   ├── sqlite_repo.py   # 오답노트 DB 처리
│   │   └── faiss_repo.py    # 문서 임베딩 및 벡터 검색
│   ├── llm_services/        # AI 모델 통신
│   │   ├── prompt_manager.py# 프롬프트 제어
│   │   └── langchain_client.py # Gemini, Ollama API 연동
│   └── document_parser/     # 문서 처리
│       └── pdf_parser.py    # PyMuPDF 연동 및 Chunking
├── presentation/            # [UI 계층]
│   └── ui_components.py     # Streamlit 위젯 렌더링
└── main.py                  # [의존성 주입 및 진입점] 객체 조립 및 실행
```

### 2.2 계층별 역할 및 책임 (의존성 규칙)
* **안쪽 계층(Domain, Use Cases)은 바깥쪽 계층(UI, DB, LangChain)을 전혀 알지 못해야 합니다.**
* **Domain Layer**: Streamlit이나 LangChain 모듈을 import하지 않는 순수한 Python 객체(Pydantic/Dataclass)입니다.
* **Use Cases Layer**: "PDF 업로드 -> 텍스트 파싱 -> 임베딩 -> 문제 생성" 이라는 일련의 순서(흐름)만 제어하며, 세부적인 파싱 방법이나 통신 방법은 어댑터에 위임합니다.
* **Interface Adapters**: PyMuPDF 문법, LangChain 문법, SQLite SQL 문법 등 특정 기술에 종속적인 코드가 여기에 모입니다.

---

## 3. 핵심 기능 및 문맥 단절 방어 로직 (Interface Adapters에서 구현)

클린 아키텍처의 `interface_adapters` 계층에서 다음의 4대 방어 로직을 책임지고 구현합니다.

1. **Chunk Overlap (오버랩) 적용**: `pdf_parser.py`에서 텍스트 분할 시 앞뒤 단락이 겹치도록 설정.
2. **Multi-Chunk 병합 (Top-K)**: `faiss_repo.py`에서 연관된 조각(Top-K)을 합쳐서 리턴.
3. **Parent Document Retriever**: `faiss_repo.py`에서 정밀 검색 후 상위 단락 반환 기능 구현.
4. **엄격한 프롬프트 제어**: `prompt_manager.py`에 강제 제약 조건 명시.

---

## 4. TDD (Test-Driven Development) 적용 전략

이 프로젝트는 클린 아키텍처를 채택하고 있으므로, 계층이 완벽히 분리되어 있어 **TDD(테스트 주도 개발)**를 적용하기에 최적의 환경입니다.

* **테스트 도구**: `pytest` 및 `pytest-mock`을 활용합니다.
* **디렉토리 구조**: 프로젝트 루트에 `tests/` 폴더를 생성하고, 내부적으로 `domain/`, `use_cases/`, `interface_adapters/` 단위로 철저히 격리된 테스트를 작성합니다.
* **개발 프로세스 (Red-Green-Refactor)**:
  1. 외부 프레임워크와 무관한 Use Case 및 Domain 로직에 대한 테스트 코드를 먼저 작성합니다. (Fail)
  2. 해당 테스트를 통과할 수 있는 코드를 구현합니다. (Pass)
  3. LLM API 연동(Gemini)이나 데이터베이스(FAISS, SQLite) 같은 무거운 I/O 작업은 `unittest.mock`을 사용하여 가짜 객체(Mock)로 대체하여 테스트 속도와 독립성을 확보합니다.

---

## 5. 데이터베이스 스키마 (SQLite)
* `incorrect_answers`: `[id, question_text, options, user_answer, correct_answer, explanation, created_at]`

---

## User Review Required

클린 아키텍처와 결합된 TDD는 **비즈니스 로직의 안정성을 보장**하고 **버그를 사전에 차단**하는 아주 강력한 무기입니다!

1. 개발 환경에 `pytest` 패키지를 추가하고,
2. 아직 작성하지 않은 `use_cases` 및 `faiss_repo`, `langchain_client` 코드들을 **테스트 코드부터 작성한 뒤 구현하는 TDD 방식**으로 전환할까요?
