# 🤖 AI 학습 도우미 챗봇 (Clean Architecture 기반)

이 프로젝트는 PDF 문서를 기반으로 4지선다 문제를 출제하고, 오답 노트를 관리하며, 실시간 질의응답이 가능한 AI 학습 도우미 애플리케이션입니다. **클린 아키텍처(Clean Architecture)** 패턴을 도입하여 핵심 비즈니스 로직과 UI, 외부 프레임워크(LLM, DB)와의 결합도를 최소화하고, 높은 유지보수성과 확장성을 자랑합니다.

---

## 🌟 주요 기능

1. **PDF 교재 인덱싱 (RAG)**
   - PyMuPDF를 활용한 PDF 파싱 및 텍스트 청킹 (Chunk Overlap 방어 로직 적용)
   - 로컬 `Ollama (bge-m3)` 모델을 이용한 임베딩 생성 및 `FAISS` 벡터 DB 저장
2. **AI 문제 출제 모드**
   - 교재 문맥 기반 무작위 4지선다 문제 생성 (`Gemini-3.1-flash-lite`)
   - 엄격한 프롬프트 제어 및 구조화된 데이터(Pydantic) 출력을 통한 환각 방어
   - 사용자가 문제를 풀고 정답/해설 즉시 확인
3. **오답 노트 관리**
   - 틀린 문제는 내장 `SQLite` 데이터베이스에 자동으로 저장
   - 저장된 문제와 본인이 선택했던 오답, 정답, 해설을 한눈에 복습 가능
4. **실시간 질의응답 챗봇 (Q&A)**
   - 교재 내용에 대한 질문을 입력하면, FAISS 검색 결과를 기반으로 RAG(Retrieval-Augmented Generation)를 수행하여 답변 제공
   - 교재에 없는 내용은 답변하지 않도록 통제됨

---

## 🛠 기술 스택

- **언어**: Python (>= 3.12)
- **UI 프레임워크**: Streamlit
- **LLM / AI 연동**: LangChain, Google Gemini API, Ollama (임베딩)
- **문서 파싱**: PyMuPDF (`fitz`)
- **데이터베이스**: FAISS (Vector DB), SQLite (RDBMS)
- **테스트**: `pytest`, `pytest-mock` (TDD 기반 개발)
- **패키지 매니저**: `uv`

---

## 📂 디렉토리 구조 (클린 아키텍처)

```text
ch16/
├── domain/                  # [도메인 엔티티] Pydantic 기반 순수 데이터 모델 (Question, DocumentChunk 등)
├── use_cases/               # [유스케이스] 핵심 애플리케이션 비즈니스 로직 제어 (문제 생성, QA, 오답노트 흐름)
├── interface_adapters/      # [어댑터] 외부 인터페이스 (DB, API, 파일 시스템) 연동
│   ├── document_parser/     # PyMuPDF 연동 PDF 파싱 및 Chunk 분할
│   ├── llm_services/        # LangChain & Gemini API 통신 구현
│   └── repositories/        # FAISS 벡터 DB 및 SQLite 기반 저장소 구현
├── presentation/            # [프레젠테이션 계층] Streamlit UI 구성 및 뷰 로직
├── tests/                   # 단위 테스트 (pytest 기반 Red-Green-Refactor)
└── main.py                  # 진입점 및 의존성 주입(DI) 컨테이너 역할
```

---

## 🚀 설치 및 구동 방법

### 1. 사전 요구사항(Prerequisites)
- [Ollama](https://ollama.com/)가 로컬에 설치되어 구동 중이어야 합니다.
- Ollama 임베딩 모델 `bge-m3` 다운로드:
  ```bash
  ollama run bge-m3
  ```
- Google Gemini API 키 발급이 필요합니다.

### 2. 프로젝트 클론 및 환경 변수 설정
프로젝트 폴더에서 `.env` 파일을 생성하고 발급받은 Gemini API 키를 입력하세요.
```env
# .env 파일
GOOGLE_API_KEY=당신의_제미나이_API_키를_입력하세요
```

### 3. 패키지 설치
이 프로젝트는 초고속 패키지 관리자인 `uv`를 권장합니다. (기존 pip/venv 사용 가능)
```bash
# uv를 이용한 설치 및 가상환경 구성
uv sync
```

### 4. 애플리케이션 실행
터미널에서 아래 명령어를 입력하여 Streamlit 앱을 실행합니다.
```bash
uv run streamlit run main.py
```
브라우저가 열리면 좌측 사이드바에서 PDF 교재를 업로드하여 기능을 이용해 보세요!

---

## ✅ 단위 테스트 실행

프로젝트 전반에 걸친 비즈니스 로직과 어댑터 동작을 검증하려면 아래 명령어를 통해 테스트를 실행할 수 있습니다.
```bash
uv run pytest
```
