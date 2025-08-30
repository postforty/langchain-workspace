# 스트림릿 실행 방법: uv run streamlit run 01_streamlit.py
import streamlit as st

st.title("나만의 챗봇 만들기")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.chat_input("무엇이 궁궁하신가요?")

# print(user_input)

if user_input:
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(user_input)

    st.session_state["messages"].append(("user", user_input))
    st.session_state["messages"].append(("assistant", user_input))

print("st.session_state.messages:", st.session_state.messages)