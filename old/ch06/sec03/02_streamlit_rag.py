import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

vectorstore = FAISS.load_local(
    "./faiss_index",
    embeddings,
    allow_dangerous_deserialization=True # 데이터 역직렬화 허용
)

retriever = vectorstore.as_retriever()

from langchain.tools import tool

@tool
def search_documents(query: str) -> str:
    """테크노빌드 주식회사(TechnoBuild) 임직원 통합 가이드북 검색 도구입니다."""
    docs = retriever.invoke(query)

    print("\n\n--- docs.page_content ---")
    for doc in docs:
        print(doc.page_content)
    print("--- docs.page_content ---\n\n")

    return "\n\n".join([doc.page_content for doc in docs])

st.title("나의 첫 챗봇 🤖")

st.caption("첫 번째 챗봇 마크-1")

with st.sidebar:
    clear_btn = st.button("초기화")

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
    system_prompt = """당신은 테크노빌드 주식회사 가이드북 정보를 친절하게 제공하는 어시스턴트입니다.

1. 정보가 필요할 경우 반드시 검색 도구를 사용하여 확인하세요.
2. 답변은 반드시 검색된 문서의 내용에만 기반하여 작성하세요.
3. 문서에 관련 내용이 없다면 억지로 꾸며내지 말고 모른다고 답변하세요.
"""
    agent = create_agent(
        model="google_genai:gemini-3-flash-preview",
        tools=[search_documents],
        system_prompt=system_prompt
    )

    def extract_ai_msg(data):
        if isinstance(data, dict) and "messages" in data:
            return data["messages"][-1]
        return AIMessage(content="")

    def extract_text(msg):
        if hasattr(msg, "content"):
            content = msg.content
            if isinstance(content, list) and len(content) > 0:
                if isinstance(content[0], dict) and "text" in content[0]:
                    return content[0]["text"]
            return content
        return str(msg)

    output_parser = StrOutputParser()

    chain = agent | extract_ai_msg | extract_text | output_parser

    return chain

print_messages()

if prompt := st.chat_input("궁금한 내용을 물어보세요!"):
    st.chat_message("user").markdown(prompt)
    add_message("user", prompt)

    chain = create_chain()

    res = chain.invoke({"messages": st.session_state.messages})

    st.chat_message("assistant").markdown(res)

    add_message("assistant", res)
