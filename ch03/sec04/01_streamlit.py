import streamlit as st

st.title("나만의 챗봇 🤖")

st.caption("뭐든지 답변하는 나만의 챗봇 만들기!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(message)

if prompt := st.chat_input("궁금한 내용을 물어보세요!"):
    st.chat_message("user").write(prompt)
    st.chat_message("assistant").write(prompt + "에 대한 답변!")

    st.session_state.messages.append(("user", prompt))
    st.session_state.messages.append(("assistant", prompt + "에 대한 답변!"))
