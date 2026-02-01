from mcp.server.fastmcp import FastMCP
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
import yfinance as yf

mcp = FastMCP("Simple MCP Server")

@mcp.tool()
def hello(name: str) -> str:
    """간단한 인사말을 반환하는 도구"""
    return f"안녕하세요, {name}님!"

# 1. 타입 힌팅
# 2. doc-string
# 3. 데코레이터

@mcp.tool()
def get_current_time(timezone: str, location: str) -> str:
    """현재 시각을 반환하는 함수

    Args:
        timezone (str): 타임존 (예: Asia/Seoul) 실제 존재하는 타임존이어야 함
        location (str): 지역명. 타임존이 모든 지명에 대응되지 않기 때문에 이후 LLM 답변 생성에 사용됨
    """
    target_timezone = ZoneInfo(timezone)

    now = datetime.now(target_timezone).strftime("%Y-%m-%d %H:%M:%S")
    location_and_local_time = f"{timezone} ({location}) 현재 시각 {now}"

    print(location_and_local_time)

    return location_and_local_time

class StockHistoryInput(BaseModel):
    ticker: str = Field(..., title="주식 코드", description="주식 코드 (예: TSLA)")
    period: str = Field(..., title="기간", description="주식 데이터 조회 기간 (예: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")

@mcp.tool()
def get_yf_stock_history(stock_history_input: StockHistoryInput) -> str:
    """주식 종목의 가격 데이터를 조회하는 함수"""
    stock = yf.Ticker(stock_history_input.ticker)
    history = stock.history(period=stock_history_input.period)
    return history.to_markdown()

@mcp.tool()
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

@mcp.resource("simple://info")
def get_server_info() -> str:
    """서버 정보를 제공하는 리소스"""
    return """
======================
Simple MCP Server 정보
======================

이 서버는 MCP의 기본 기능을 시연하는 간단한 예제입니다.
"""

mcp.run(transport='streamable-http')