import streamlit as st
from langchain.messages import AIMessage, HumanMessage

st.title("나만의 챗봇 만들기")

if "messages" not in st.session_state:
    st.session_state.messages = []

def print_messages():
    for message in st.session_state.messages:
        if message.type == "human":
            st_role = "user";
        if message.type == "ai":
            st_role = "assistant"
        
        st.chat_message(st_role).markdown(message.content)

def add_message(role, message):
    if role == "user":
        st.session_state.messages.append(HumanMessage(content=message))
    elif role == "assistant":
        st.session_state.messages.append(AIMessage(content=message))
    else:
        return
    
print_messages()

if prompt := st.chat_input("궁금한 내용을 물어보세요!"):
    st.chat_message("user").markdown(prompt)
    st.chat_message("assistant").markdown(prompt + "에 대한 답변!")

    add_message("user", prompt)
    add_message("assistant", prompt + "에 대한 답변!")


