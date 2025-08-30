# 랭체인 적용
import streamlit as st
from langchain_core.messages.chat import ChatMessage

st.title("나만의 챗봇 만들기")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

print_messages()

def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

user_input = st.chat_input("무엇이 궁궁하신가요?")

# print(user_input)

if user_input:
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(user_input)

    add_message("user", user_input)
    add_message("assistant", user_input)

print("st.session_state.messages:", st.session_state.messages)