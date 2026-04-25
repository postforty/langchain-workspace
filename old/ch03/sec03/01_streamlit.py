import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

st.title("나의 첫 챗봇 🤖")

st.caption("첫 번째 챗봇 마크-0")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [AIMessage(content="무엇이든 물어 보세요! 👇")]

def print_messages():
    for lang_message in st.session_state["messages"]:
        if lang_message.type == "human":
            st_role = "user"
        elif lang_message.type == "ai":
            st_role = "assistant"
        else:
            st_role = "assistant"
        
        st.chat_message(st_role).markdown(lang_message.content)

def add_message(role, message):
    if role == "user":
        msg_obj = HumanMessage(content=message)
    elif role == "assistant":
        msg_obj = AIMessage(content=message)
    else:
        return
    
    st.session_state["messages"].append(msg_obj)

print_messages()

if prompt := st.chat_input("궁금한 내용을 물어보세요!"):
    st.chat_message("user").markdown(prompt)
    st.chat_message("assistant").markdown(prompt)

    add_message("user", prompt)
    add_message("assistant", prompt)
