import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver

from langchain.tools import tool 
from langchain.agents import create_agent 
from datetime import datetime 
from zoneinfo import ZoneInfo 
from pydantic import BaseModel, Field 
import yfinance as yf 
from langchain_community.tools import DuckDuckGoSearchResults 
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper 

from dotenv import load_dotenv
load_dotenv()

st.title("🛠️ [실습] 도구 호출 챗봇 만들기")
st.caption("도구를 직접 정의하고 에이전트에 연결해 보세요!")

# 세션 상태 초기화
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(datetime.now().timestamp())

# =================================================================
# [실습 1] 시계 도구 구현하기
# =================================================================
@tool
def get_current_time(timezone: str, location: str) -> str:
    """ 현재 시각을 반환하는 함수

    Args:
        timezone (str): 타임존 (예: 'Asia/Seoul') 실제 존재하는 타임존이어야 함
        location (str): 지역명. 타임존이 모든 지명에 대응되지 않기 때문에 이후 model 답변 생성에 사용됨
    """
    target_timezone = ZoneInfo(timezone)
    now = datetime.now(tz=target_timezone).strftime("%Y-%m-%d %H:%M:%S")
    location_and_local_time = f"{timezone} ({location}) 현재시각 {now}"
    return location_and_local_time

# =================================================================
# [실습 2] 주가 검색 도구 구현하기 (Pydantic 모델 활용)
# =================================================================
class StockHistoryInput(BaseModel):
    ticker: str = Field(..., title="주식 코드", description="주식 코드 (예: TSLA)")
    period: str = Field(..., title="기간", description="주식 데이터 조회 기간 (예: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)")

@tool
def get_yf_stock_history(stock_history_input: StockHistoryInput) -> str:
    """ 주식 종목의 가격 데이터를 조회하는 함수"""
    stock = yf.Ticker(stock_history_input.ticker)
    history = stock.history(period=stock_history_input.period)
    return history.to_markdown()

# =================================================================
# [실습 3] 웹 검색 도구 구현하기 (DuckDuckGo 활용)
# =================================================================
@tool
def get_web_search(query: str, search_period: str='w', region: str='kr-kr') -> str:
    """
    특정 지역과 기간을 설정하여 웹 검색(뉴스)을 수행합니다.

    Args:
        query (str): 검색어
        search_period (str): 검색 기간. 'd'(일간), 'w'(주간), 'm'(월간), 'y'(연간) 중 선택
        region (str): 검색 지역 코드. 한국('kr-kr'), 미국('us-en') 등
    """
    wrapper = DuckDuckGoSearchAPIWrapper(
        region=region,
        time=search_period
    )

    search = DuckDuckGoSearchResults(
        api_wrapper=wrapper,
        results_separator=";\n"
    )

    return search.invoke(query)

# 메시지 및 체인 초기화 로직 (준비됨)
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "chain" not in st.session_state:
    st.session_state["chain"] = None

def clear_task():
    st.session_state["messages"] = []
    st.session_state["chain"] = None
    st.session_state["thread_id"] = str(datetime.now().timestamp())
    
with st.sidebar:  
    st.button("대화 초기화", on_click=clear_task)

def print_messages():
    for chat_message in st.session_state["messages"]:
        if isinstance(chat_message, HumanMessage):
            with st.chat_message("user"):
                st.write(chat_message.content)
        elif isinstance(chat_message, AIMessage):
            with st.chat_message("assistant"):
                st.write(chat_message.content)

def add_message(role, message):
    if role == "user":
        st.session_state["messages"].append(HumanMessage(content=message))
    elif role == "assistant":
        st.session_state["messages"].append(AIMessage(content=message))

# =================================================================
# [실습 4] 에이전트 체인 생성 함수 완성하기
# =================================================================
def create_chain():
    # 1. 위에서 정의한 도구들을 리스트로 묶으세요.
    tools = [get_current_time, get_yf_stock_history, get_web_search]

    # 2. create_agent 함수를 사용하여 에이전트를 생성하고 반환하세요.
    # - model: "google_genai:gemini-2.5-flash"
    # - tools: 위에서 만든 도구 리스트
    # - checkpointer: InMemorySaver()
    return create_agent(
        model="google_genai:gemini-2.5-flash", 
        tools=tools, 
        checkpointer=InMemorySaver()
    )

# 실행 로직
print_messages()

if st.session_state["chain"] is None:
    st.session_state["chain"] = create_chain()

if user_input := st.chat_input("질문을 입력하세요!"):
    if st.session_state["chain"] is not None:
        st.chat_message("user").write(user_input)
        add_message("user", user_input)

        with st.chat_message("assistant"):
            ai_container = st.empty()
            with st.status("답변을 생성하고 있습니다...", expanded=True) as status:
                final_state = None
                # [실습 5] st.session_state["chain"].stream()을 사용하여 답변을 수집하세요.
                # config에는 {"configurable": {"thread_id": st.session_state["thread_id"]}}를 전달하세요.
                for state in st.session_state["chain"].stream(
                    {"messages": [{"role": "user", "content": user_input}]},
                    {"configurable": {"thread_id": st.session_state["thread_id"]}},
                    stream_mode="values"
                ):
                    final_state = state
                    # 도구 호출 상태 출력 로직
                    last_msg = state["messages"][-1]
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        for tool_call in last_msg.tool_calls:
                            status.write(f"🛠️ `{tool_call['name']}` 도구를 실행 중입니다...")
                
                status.update(label="답변 완료!", state="complete", expanded=False)

            # 최종 답변 추출 및 출력
            if final_state:
                last_message = final_state["messages"][-1]
                ai_content = last_message.content if isinstance(last_message.content, str) else str(last_message.content)
                ai_container.write(ai_content)
                add_message("assistant", ai_content)