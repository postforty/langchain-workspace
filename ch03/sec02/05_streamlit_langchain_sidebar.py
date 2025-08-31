# 랭체인 LCEL 적용
import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


st.title("나만의 챗봇 만들기")

with st.sidebar:
    clear_btn = st.button("대화 초기화")

    selected_prompt = st.selectbox(
        "언어를 선택해 주세요", ("Korean", "English"), index=0
    )

# print("clear_btn:", clear_btn)
# print("selected_prompt:", selected_prompt)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if clear_btn:
    st.session_state["messages"] = []

def create_chain():
    print("selected_prompt:", selected_prompt)

    if selected_prompt == "Korean":
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "당신은 한국어로 대답하는 친절한 AI 어시스턴트입니다."),
                ("user", "#Question:\n{question}")
            ]
        )

    if selected_prompt == "English":
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a friendly AI assistant who answers in English. Please make sure to answer Korean questions in English."),
                ("user", "#Question:\n{question}")
            ]
        )
    
    print("prompt:", prompt)

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=gemini_api_key
    )

    output_parsers = StrOutputParser()

    chain = prompt | llm | output_parsers

    return chain

def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

print_messages()

def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

user_input = st.chat_input("무엇이 궁궁하신가요?")

if user_input:
    st.chat_message("user").write(user_input)
    add_message("user", user_input)

    chain = create_chain()

    # 답변이 완전히 생성되면 출력
    # response = chain.invoke({"question": user_input})
    # print("response:", type(response), response)
    # st.chat_message("assistant").write(response)
    # add_message("assistant", response)

    # 타이핑하듯이 답변 출력
    response = chain.stream({"question": st.session_state.messages})
    with st.chat_message("assistant"):
        container = st.empty() # 페이지 전체를 다시 로드하지 않고 콘텐츠를 동적으로 업데이트하는 빈 컨테이너 생성

        ai_answer = ""

        for token in response:
            ai_answer += token
            container.markdown(ai_answer)
        
    add_message("assistant", ai_answer)

# print("st.session_state.messages:", st.session_state.messages)



