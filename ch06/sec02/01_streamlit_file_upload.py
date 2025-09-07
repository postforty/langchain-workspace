import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, load_prompt
import glob

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if "task_input" not in st.session_state:
    st.session_state["task_input"] = ""

st.title("PDF 기반 Q&A")

if not os.path.exists(".cache"):
    os.mkdir(".cache")

if not os.path.exists(".cache/files"):
    os.mkdir(".cache/files")

if not os.path.exists(".cache/embeddings"):
    os.mkdir(".cache/embeddings")

@st.cache_resource(show_spinner="업로드한 파일을 처리 중입니다...")
def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)

def clear_task():
    st.session_state["messages"] = []

with st.sidebar:
    st.button("대화 초기화", on_click=clear_task)

    uploaded_file = st.file_uploader("파일 업로드", type=["pdf"])

    selected_prompt = "prompts/pdf-rag.yaml"

# print("clear_btn:", clear_btn)
# print("selected_prompt:", selected_prompt)
# print("uploaded_file:", uploaded_file)

if uploaded_file:
    embed_file(uploaded_file)

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
def create_chain(prompt_filepath):
    prompt = load_prompt(prompt_filepath, encoding="utf-8")
    
    print("prompt:", prompt)

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=gemini_api_key
    )

    output_parsers = StrOutputParser()

    chain = prompt | llm | output_parsers

    return chain

def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

print_messages()

def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

user_input = st.chat_input("무엇이 궁궁하신가요?")

if user_input:
    st.chat_message("user").write(user_input)
    add_message("user", user_input)

    chain = create_chain(selected_prompt)

    # 답변이 완전히 생성되면 출력
    # response = chain.invoke({"question": user_input})
    # print("response:", type(response), response)
    # st.chat_message("assistant").write(response)
    # add_message("assistant", response)

    # 타이핑하듯이 답변 출력
    response = chain.stream({"question": st.session_state.messages})
    with st.chat_message("assistant"):
        container = st.empty() # 페이지 전체를 다시 로드하지 않고 콘텐츠를 동적으로 업데이트하는 빈 컨테이너 생성

        ai_answer = ""

        for token in response:
            ai_answer += token
            container.markdown(ai_answer)
        
    add_message("assistant", ai_answer)

# print("st.session_state.messages:", st.session_state.messages)



