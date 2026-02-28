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

st.title("🛠️ 도구 & 메모리 실습 챗봇")
st.caption("안내에 따라 TODO 부분을 채워 기능을 완성해 보세요!")

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(datetime.now().timestamp())

@tool
def get_current_time(timezone: str, location: str) -> str:
    """ 현재 시각을 반환하는 함수
    Args:
        timezone (str): 타임존 (예: 'Asia/Seoul')
        location (str): 지역명
    """
    target_timezone = ZoneInfo(timezone)
    now = datetime.now(target_timezone).strftime("%Y-%m-%d %H:%M:%S")
    return f'{timezone} ({location}) 현재시각 {now}'

class StockHistoryInput(BaseModel):
    ticker: str = Field(..., title="주식 코드", description="주식 코드 (예: TSLA)")
    period: str = Field(..., title="기간", description="주식 데이터 조회 기간 (예: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")

@tool
def get_yf_stock_history(stock_history_input: StockHistoryInput) -> str:
    """주식 종목의 가격 데이터를 조회하는 함수"""
    stock = yf.Ticker(stock_history_input.ticker)
    history = stock.history(period=stock_history_input.period)
    return history.to_markdown()

@tool
def get_web_search(query: str, serach_period: str='w', region: str="kr-kr") -> str:
    """특정 지역과 기간을 설정하여 웹 검색을 수행합니다.
    
    Args:
        query (str): 검색어
        serach_period (str): 검색 기간. 'd'(일간), 'w'(주간), 'm'(월간), 'y'(연간) 중 선택
        region (str): 검색 지역 코드. 한국('kr-kr'), 미국('us-en')
    
    Returns:
        str: 검색된 결과
    """
    wrapper = DuckDuckGoSearchAPIWrapper(region=region, time=serach_period)

    search = DuckDuckGoSearchResults(api_wrapper=wrapper, results_separator=";\n")

    return search.invoke(query)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "chain" not in st.session_state:
    st.session_state["chain"] = None

def clear_task():
    st.session_state["messages"] = []
    st.session_state["chain"] = None
    # TODO: 대화 초기화 시 thread_id도 새롭게 갱신해 보세요.
    
with st.sidebar:  
    st.button("대화 초기화", on_click=clear_task)

def create_chain():
    tools = [get_current_time, get_yf_stock_history, get_web_search] 

    return create_agent(
        model="google_genai:gemini-3-flash-preview", 
        tools=tools,
        checkpointer=InMemorySaver()
    )

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

if user_input := st.chat_input("질문을 입력하세요!"):
    st.chat_message("user").write(user_input)
    st.session_state["messages"].append(HumanMessage(content=user_input))

    with st.chat_message("assistant"):
        ai_container = st.empty()

        with st.status("답변 생성 중...", expanded=True) as status:
            final_state = None
            for state in st.session_state["chain"].stream(
                {"messages": [{"role": "user", "content": user_input}]},
                {"configurable": {"thread_id": st.session_state["thread_id"]}},
                stream_mode="values"
            ):
                final_state = state
                print("final_state:", final_state)
                last_msg = state["messages"][-1]
                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                    for tool_call in last_msg.tool_calls:
                        status.write(f"🛠️ {tool_call['name']} 도구를 실행 중입니다...")
                
            status.update(label="답변 완료!", state="complete", expanded=False)

        if final_state:
            last_message = final_state["messages"][-1]
            ai_content = ""

            if isinstance(last_message.content, str):
                ai_content = last_message.content
            elif isinstance(last_message.content, list):
                for content_part in last_message.content:
                    if isinstance(content_part, dict) and content_part.get("type") == "text":
                        ai_content += content_part.get("text", "")
                    elif isinstance(content_part, str):
                        ai_content += content_part

            ai_container.write(ai_content)