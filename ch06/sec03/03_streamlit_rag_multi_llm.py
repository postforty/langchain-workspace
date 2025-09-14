import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, load_prompt
# from langchain_community.document_loaders import PyPDFLoader # gemini embedding 모델 quota 오류 발생
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM

import shutil # 파일 및 디렉토리 작업용
import uuid # 고유 키 생성

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

st.title("PDF 기반 Q&A")
st.caption("Ollama BGE-M3 + Multi LLM") # 캡션 추가

if not os.path.exists(".cache"):
    os.mkdir(".cache")
    # 윈도우에서 .cache 폴더를 숨김 처리
    if os.name == 'nt':
        os.system('attrib +h .cache')

if not os.path.exists(".cache/files"):
    os.mkdir(".cache/files")

if not os.path.exists(".cache/embeddings"):
    os.mkdir(".cache/embeddings")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "chain" not in st.session_state:
    st.session_state["chain"] = None

# * 헬퍼 함수 정의
# 벡터스토어 생성 또는 로드
def _get_or_create_vectorstore(file_name, splitted_documents=None):
    # 임베딩 모델 준비
    # gemini-embedding-001 모델은 QUOTA 오류 발생할 수 있음
    # 참고) https://ai.google.dev/gemini-api/docs/rate-limits?hl=ko
    # embedding_model = GoogleGenerativeAIEmbeddings(
    #     model="gemini-embedding-001",
    #     google_api_key=gemini_api_key,
    #     transport='rest' # Streamlit의 동기적인 환경과 호환되도록 설정(기본값은 비동기)
    # )

    embedding_model = OllamaEmbeddings(model="bge-m3", base_url="http://localhost:11434")

    embedding_path = f".cache/embeddings/{file_name}"
    vectorstore = None
    if splitted_documents is not None:  # If new documents are provided, always create
        print(f"FAISS 인덱스 {embedding_path}를 생성합니다.")
        if os.path.exists(embedding_path):  # Remove old one if exists
            shutil.rmtree(embedding_path)
        vectorstore = FAISS.from_documents(splitted_documents, embedding_model)
        vectorstore.save_local(embedding_path)
        print(f"FAISS 인덱스를 {embedding_path}에 저장했습니다.")
    elif os.path.exists(embedding_path):  # Otherwise, try to load existing
        print(f"FAISS 인덱스 {embedding_path}를 로드합니다.")
        vectorstore = FAISS.load_local(
            embedding_path,
            embedding_model,
            allow_dangerous_deserialization=True,
        )

    return vectorstore

@st.cache_resource(show_spinner="업로드한 파일을 처리 중입니다...", ttl=3600) # 1시간 동안 캐싱
def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)

    # 문서 로드
    # loader = PyPDFLoader(file_path)
    loader = PyMuPDFLoader(file_path)
    pages = loader.load()

    # 문서 분할
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # 최대 길이(1000자 이하)
        chunk_overlap=200 # 정확히 200자 중첩
    )
    chunks = splitter.split_documents(pages)

    # 벡터스토어 생성 또는 로드
    vectorstore = _get_or_create_vectorstore(file.name, chunks)

    retriever = vectorstore.as_retriever()

    return retriever
   
def create_chain(retriever, prompt_filepath, model_name):
    prompt = load_prompt(prompt_filepath, encoding="utf-8")
    
    print("model_name:", model_name)

    if model_name.startswith("gemini"):
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0,
            google_api_key=gemini_api_key)
    else:
        llm = OllamaLLM(
            model=model_name, 
            base_url="http://localhost:11434")

    output_parser = StrOutputParser()

    chain = (
        {"context": retriever, "question": RunnablePassthrough()} 
        | prompt 
        | llm 
        | output_parser
    )

    return chain

def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

def clear_task():
    st.session_state["messages"] = []
    st.session_state["chain"] = None

    # 파일 업로드 UI 초기화
    st.session_state.file_uploader_key = str(uuid.uuid4()) # 초기화 버튼 관련 고유한 키로 업데이트
    st.session_state.uploaded_file = None

    # 기존 업로드 파일 및 벡터 스토어 삭제 및 비어 있는 폴더 생성
    if os.path.exists(".cache/files"):
        shutil.rmtree(".cache/files")
    if os.path.exists(".cache/embeddings"):
        shutil.rmtree(".cache/embeddings")
    os.makedirs(".cache/files")
    os.makedirs(".cache/embeddings")

with st.sidebar:
    clear_btn = st.button("대화 초기화", on_click=clear_task)

    # 파일 업로드 UI 초기화
    # - 초기화 버튼 클릭시 삭제하기 위해 고유키로 관리
    if 'file_uploader_key' not in st.session_state:
        st.session_state.file_uploader_key = str(uuid.uuid4())
    uploaded_file = st.file_uploader("파일 업로드", type=["pdf"], key=st.session_state.file_uploader_key) 

    selected_prompt = "prompts/pdf-rag.yaml"

    selected_model = st.selectbox(
        "LLM 선택",
        ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite", "gemma3:latest"],
        index=1
    )

# * 프로그램 시작 시 또는 다시 시작될 때 기존 벡터 저장소 로드
if st.session_state["chain"] is None:
    embedding_files = [f for f in os.listdir(
        ".cache/embeddings") if os.path.isdir(os.path.join(".cache/embeddings", f))]

    print("embedding_files:", embedding_files)

    if embedding_files:
        # 첫 번째 발견된 임베딩 파일을 로드
        first_embedding_file = embedding_files[0]
        vectorstore = _get_or_create_vectorstore(first_embedding_file)
        if vectorstore:
            retriever = vectorstore.as_retriever()
            st.session_state["chain"] = create_chain(
                retriever, selected_prompt, selected_model)
            st.success(f"기존 벡터 저장소 '{first_embedding_file}'를 로드했습니다.")

if uploaded_file:
    retriever = embed_file(uploaded_file)
    chain = create_chain(retriever, selected_prompt, selected_model)
    st.session_state["chain"] = chain

print_messages()

warning_msg = st.empty()

user_input = st.chat_input("무엇이 궁궁하신가요?")

if user_input:
    chain = st.session_state["chain"]

    if chain is not None:
        st.chat_message("user").write(user_input)
        response = chain.stream(user_input)
        
        with st.chat_message("assistant"):
            container = st.empty() # 페이지 전체를 다시 로드하지 않고 콘텐츠를 동적으로 업데이트하는 빈 컨테이너 생성

            ai_answer = ""

            for token in response:
                ai_answer += token
                container.markdown(ai_answer)
        
        add_message("user", user_input)
        add_message("assistant", ai_answer)
    else:
        warning_msg.error("파일을 업로드해 주세요.")

# print("st.session_state.messages:", st.session_state.messages)



