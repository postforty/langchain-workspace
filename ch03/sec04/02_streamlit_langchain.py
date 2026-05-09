import streamlit as st
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()

st.title("나만의 챗봇 🤖")

st.caption("뭐든지 답변하는 나만의 챗봇 만들기!")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    clear_btn = st.button("초기화")

    selected_prompt = st.selectbox(
        "언어를 선택해 주세요", 
        ("한국어", "English"), 
        index=0
    )

# print("selected_prompt:", selected_prompt)
# print("clear_btn:", clear_btn)

if clear_btn:
    st.session_state.messages = []

def print_messages():
    for message in st.session_state.messages:
        if message.type == "human":
            st_role = "user"
        
        if message.type == "ai":
            st_role = "assistant"
        
        st.chat_message(st_role).markdown(message.content)

def add_message(role, message):
    if role == "user":
        msg_obj = HumanMessage(content=message)
    if role == "assistant":
        msg_obj = AIMessage(content=message)

    st.session_state.messages.append(msg_obj)

def create_chain():
    if selected_prompt == "한국어":
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage("당신은 한국어로 대답하는 친절하고 도움이 되는 AI 어시스턴트입니다."),
                MessagesPlaceholder(variable_name="messages")
            ]
        )

    if selected_prompt == "English":
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage("당신은 영어로 대답하는 친절하고 도움이 되는 AI 어시스턴트입니다. 답변은 반드시 영어로 해야합니다."),
                MessagesPlaceholder(variable_name="messages")
            ]
        )

    model = init_chat_model("google_genai:gemini-3.1-flash-lite")

    chain = prompt | model | StrOutputParser()

    return chain

print_messages()

if prompt := st.chat_input("궁금한 내용을 물어보세요!"):
    st.chat_message("user").write(prompt)
    add_message("user", prompt)

    chain = create_chain()

    response = chain.invoke({"messages": st.session_state.messages})

    st.chat_message("assistant").write(response)
    add_message("assistant", response)