# 스트림릿 실행 방법: uv run streamlit run 01_streamlit.py
import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

st.title("나만의 챗봇 만들기")

if "chat_session" not in st.session_state:
    st.session_state["chat_session"] = client.chats.create(
        model="gemini-2.5-flash")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.chat_input("무엇이 궁궁하신가요?")

# print(user_input)

def print_messages():
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])

print_messages()

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)
    
    response = st.session_state["chat_session"].send_message(message=user_input)
    # print("response:", response.text)

    st.session_state["messages"].append({"role": "assistant", "content": response.text})
    st.chat_message("assistant").write(response.text)

print("st.session_state.messages:", st.session_state.messages)