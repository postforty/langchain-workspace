# 랭체인 LCEL 적용
import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


st.title("나만의 챗봇 만들기")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def create_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "당신은 친절한 AI 어시스턴트입니다."),
            ("user", "#Question:\n{question}")
        ]
    )

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

    chain = create_chain()

    response = chain.stream({"question": user_input})

    print("response:", type(response), response)

    st.chat_message("assistant").write(response)

    add_message("assistant", response)

print("st.session_state.messages:", st.session_state.messages)



