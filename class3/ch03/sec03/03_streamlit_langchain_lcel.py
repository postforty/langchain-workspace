import streamlit as st
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import  MessagesPlaceholder, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()

st.title("🤖나만의 LangChain 챗봇 만들기")

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

def create_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="당신은 친절하고 도움이 되는 AI 어시스턴트입니다."),
            MessagesPlaceholder(variable_name="messages"),
            HumanMessagePromptTemplate.from_template("{prompt}")
        ]
    )
    model = init_chat_model("google_genai:gemini-2.5-flash")
    ouput_parser = StrOutputParser()

    chain = prompt | model | ouput_parser

    return chain
    
print_messages()

if prompt := st.chat_input("궁금한 내용을 물어보세요!"):
    st.chat_message("user").markdown(prompt)

    chain = create_chain()

    response = chain.invoke(
        {
            "messages": st.session_state.messages,
            "prompt": prompt
        }
    )

    add_message("user", prompt)
    add_message("assistant", response)

    st.chat_message("assistant").markdown(response)

