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

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

st.title("PDF 기반 Q&A")

if not os.path.exists(".cache"):
    os.mkdir(".cache")

if not os.path.exists(".cache/files"):
    os.mkdir(".cache/files")

if not os.path.exists(".cache/embeddings"):
    os.mkdir(".cache/embeddings")

def clear_task():
    st.session_state["messages"] = []

with st.sidebar:
    st.button("대화 초기화", on_click=clear_task)

    uploaded_file = st.file_uploader("파일 업로드", type=["pdf"])

    selected_prompt = "prompts/pdf-rag.yaml"

# print("clear_btn:", clear_btn)
# print("selected_prompt:", selected_prompt)
# print("uploaded_file:", uploaded_file)

@st.cache_resource(show_spinner="업로드한 파일을 처리 중입니다...")
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

    # 임베딩 모델 준비
    embeddings_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=gemini_api_key,
            # Streamlit 동기적환경과 호환되도록 설정
            # GoogleGenerativeAIEmbeddings는 기본값이 비동기이기 때문
            transport='rest'
        )

    # 임베딩
    vectorstore = FAISS.from_documents(chunks, embeddings_model)
    retriever = vectorstore.as_retriever()

    return retriever
   
def create_chain(retriever, prompt_filepath):
    prompt = load_prompt(prompt_filepath, encoding="utf-8")
    
    print("prompt:", prompt)

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=gemini_api_key
    )

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

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "chain" not in st.session_state:
    st.session_state["chain"] = None

if uploaded_file:
    retriever = embed_file(uploaded_file)
    chain = create_chain(retriever, selected_prompt)
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



