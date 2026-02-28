import streamlit as st

st.title("나만의 챗봇 만들기")

print("before:", st.session_state)

if "messages" not in st.session_state:
    st.session_state.messages = []

print("after:", st.session_state)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.chat_message("user").markdown(prompt)
    st.chat_message("assistant").markdown(prompt + "에 대한 답변!")

    st.session_state.messages.append({
        "role": "user", 
        "content": prompt
    })
    st.session_state.messages.append({
        "role": "assistant", 
        "content": prompt + "에 대한 답변!"
    })

print(st.session_state.messages)
