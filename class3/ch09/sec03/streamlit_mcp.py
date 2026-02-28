import streamlit as st
import asyncio
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver 
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent 
from datetime import datetime 
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="MCP 통합 챗봇", layout="wide")
st.title("🛠️ MCP 도구 & 메모리 실습 챗봇")
st.caption("FastMCP 서버로부터 도구를 동적으로 로드하여 대화를 수행합니다.")

# --- 비동기 도구 로드 헬퍼 함수 ---
def run_async_tools(url: str):
    """비동기 함수인 load_mcp_tools를 동기 환경에서 실행"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(load_mcp_tools(url))
    finally:
        loop.close()

# --- 세션 상태 관리 ---
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(datetime.now().timestamp())

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "chain" not in st.session_state:
    st.session_state["chain"] = None

# MCP 서버 SSE 엔드포인트
MCP_SERVER_URL = "http://localhost:8000/mcp"

def clear_task():
    """대화 초기화 및 thread_id 갱신"""
    st.session_state["messages"] = []
    st.session_state["chain"] = None
    st.session_state["thread_id"] = str(datetime.now().timestamp())
    st.rerun()

with st.sidebar:  
    st.button("대화 초기화", on_click=clear_task)
    st.info(f"Thread ID: {st.session_state['thread_id']}")
    st.write("연결 주소:", MCP_SERVER_URL)

def create_chain():
    """MCP 서버로부터 도구를 동적으로 로드하여 에이전트 생성"""
    try:
        # load_mcp_tools는 코루틴이므로 await(또는 run_until_complete)이 필수입니다.
        tools = run_async_tools(MCP_SERVER_URL)
        
        return create_agent(
            model="google_genai:gemini-3-flash-preview", 
            tools=tools,
            checkpointer=InMemorySaver()
        )
    except Exception as e:
        st.error(f"MCP 서버 연결 실패: {e}")
        return None

# 에이전트 체인 초기화
if st.session_state["chain"] is None:
    st.session_state["chain"] = create_chain()

# 메시지 출력 함수
def print_messages():
    for chat_message in st.session_state["messages"]:
        if isinstance(chat_message, HumanMessage):
            with st.chat_message("user"): st.write(chat_message.content)
        elif isinstance(chat_message, AIMessage):
            with st.chat_message("assistant"): st.write(chat_message.content)

print_messages()

# --- 채팅 로직 ---
if user_input := st.chat_input("MCP 서버의 도구에 대해 질문해 보세요!"):
    st.chat_message("user").write(user_input)
    st.session_state["messages"].append(HumanMessage(content=user_input))

    with st.chat_message("assistant"):
        ai_container = st.empty()

        if st.session_state["chain"] is None:
            st.error("에이전트가 생성되지 않았습니다. MCP 서버가 실행 중인지 확인하세요.")
            st.stop()

        with st.status("답변 생성 중...", expanded=True) as status:
            final_state = None
            # LangGraph stream을 사용하여 상태 추적
            for state in st.session_state["chain"].stream(
                {"messages": [{"role": "user", "content": user_input}]},
                {"configurable": {"thread_id": st.session_state["thread_id"]}},
                stream_mode="values"
            ):
                final_state = state
                last_msg = state["messages"][-1]
                
                # 도구 호출 시 UI에 표시
                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                    for tool_call in last_msg.tool_calls:
                        status.write(f"🛠️ MCP 도구 [**{tool_call['name']}**] 호출 중...")
                
            status.update(label="답변 완료!", state="complete", expanded=False)

        if final_state:
            last_message = final_state["messages"][-1]
            ai_content = ""

            # 응답 메시지 추출
            if isinstance(last_message.content, str):
                ai_content = last_message.content
            elif isinstance(last_message.content, list):
                for part in last_message.content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        ai_content += part.get("text", "")

            ai_container.write(ai_content)
            st.session_state["messages"].append(AIMessage(content=ai_content))