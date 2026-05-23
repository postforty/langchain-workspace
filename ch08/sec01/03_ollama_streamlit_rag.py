import streamlit as st
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

embeddings = OllamaEmbeddings(
    model="bge-m3:latest",
)

vectorstore = FAISS.load_local(
    "./faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever()

@tool
def search_documents(query: str) -> str:
    """
    테크노빌드 주식회사 임직원 통합 가이드북 검색 도구입니다.
    """
    docs = retriever.invoke(query)

    return "\n\n".join([doc.page_content for doc in docs])

st.title("📖테크노빌드 가이드 챗봇")
st.caption("테크노빌드 임직원을 위한 가이드북 챗봇입니다.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    clear_btn = st.button("초기화")

# print(clear_btn)

if clear_btn:
    st.session_state.messages = []

def print_messages():
    for lang_message in st.session_state.messages:
        st_role = "user" if lang_message.type == "human" else "assistant"
        st.chat_message(st_role).markdown(lang_message.content)

print_messages()

def add_message(role, message):
    if role == "user":
        msg_obj = HumanMessage(content=message)
    elif role == "assistant":
        msg_obj = AIMessage(content=message)
    else:
        return
    
    st.session_state.messages.append(msg_obj)

def create_chain():
    system_prompt = """당신은 테크노빌드 주식회사 가이드북 정보를 친절하게 제공하는 어시스턴트입니다.

1. 정보가 필요할 경우 반드시 검색 도구(search_documents)를 사용하여 확인하세요.
2. 답변은 반드시 검색된 문서의 내용에만 기반하여 작성하세요.
3. 문서에 관련 내용이 없다면 추측하지 말고 모른다고 답변하세요.
"""

    llm = ChatOllama(
        model="qwen3.5:4b",
        temperature=0,
    )

    agent = create_agent(
        model=llm,
        tools=[search_documents],
        system_prompt=system_prompt
    )

    print("agent", agent)

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

    chain = agent | extract_ai_msg | extract_text | StrOutputParser()

    return chain

if prompt := st.chat_input("궁금한 내용을 물어보세요!"):
    st.chat_message("user").write(prompt)
    add_message("user", prompt)

    chain = create_chain()

    response = chain.invoke(
        {"messages": st.session_state.messages}
    )

    st.chat_message("assistant").markdown(response)
    add_message("assistant", response)
