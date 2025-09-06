# 랭체인 LCEL 적용
import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, load_prompt
import glob

import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if "task_input" not in st.session_state:
    st.session_state["task_input"] = ""

st.title("나만의 LangChain 챗봇")

# print("task:", st.session_state["task_input"])

def clear_task():
    st.session_state["messages"] = []
    st.session_state["task_input"] = ""

with st.sidebar:
    st.button("대화 초기화", on_click=clear_task)

    # 파일 시스템에서 지정된 패턴과 일치하는 모든 경로명을 찾는 데 사용
    prompt_files = glob.glob("prompts/*.yaml")
    # print("prompt_files:", prompt_files)

    prompt_lables = {
        "prompts\\general.yaml": "일반 프롬프트",
        "prompts\\prompt-maker.yaml": "프롬프트 생성기",
        "prompts\\summary.yaml": "요약 프롬프트",
    }

    # selected_prompt = st.selectbox(
    #     "프롬프트를 선택해 주세요", prompt_files, index=0
    # )

    selected_prompt = st.selectbox(
        "프롬프트를 선택해 주세요", 
        prompt_files, index=0, 
        format_func=lambda x: prompt_lables.get(x, x)
    )

    task_input = st.text_input("TASK 입력", key="task_input", value=st.session_state["task_input"])

# print("clear_btn:", clear_btn)
# print("selected_prompt:", selected_prompt)

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
def create_chain(prompt_filepath, task=""):
    print("selected_prompt:", selected_prompt)


    prompt = load_prompt(prompt_filepath, encoding="utf-8")

    if task:
        prompt = prompt.partial(task=task)
    
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

    chain = create_chain(selected_prompt, task=task_input)

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



