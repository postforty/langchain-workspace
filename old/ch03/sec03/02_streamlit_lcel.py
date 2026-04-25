import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

st.title("나의 첫 챗봇 🤖")

st.caption("첫 번째 챗봇 마크-0")

with st.sidebar:
    clear_btn = st.button("초기화")

    selected_prompt = st.selectbox("언어를 선택해 주세요", ("Korean", "English"), index=0)

print(selected_prompt)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [AIMessage(content="무엇이든 물어 보세요! 👇")]

if clear_btn:
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

def create_chain():

    if selected_prompt == "Korean":
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content="당신은 한국어로 대답하는 친절한 AI 어시스턴트입니다. 답변은 반드시 한국어로 해야 합니다."),
                # HumanMessage(content={input})
                MessagesPlaceholder(variable_name='messages')
            ]
        )

    if selected_prompt == "English":
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content="당신은 영어로 대답하는 친절한 AI 어시스턴트입니다. 답변은 반드시 영어로 해야 합니다."),
                # HumanMessage(content={input})
                MessagesPlaceholder(variable_name='messages')
            ]
        )

    model = init_chat_model("google_genai:gemini-2.5-flash-lite")

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    return chain

print_messages()

if prompt := st.chat_input("궁금한 내용을 물어보세요!"):
    st.chat_message("user").markdown(prompt)
    add_message("user", prompt)

    chain = create_chain()

    res = chain.invoke({"messages": st.session_state.messages})

    st.chat_message("assistant").markdown(res)

    add_message("assistant", res)
