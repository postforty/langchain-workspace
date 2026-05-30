from fastmcp import FastMCP
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import yfinance as yf

mcp = FastMCP("My MCP Server")

@mcp.tool
def get_current_time(timezone: str, location: str) -> str:
    """
    현재 시각을 반환하는 함수

    Args:
        timezone (str): 타임존 (예: 'Asia/Seoul') 실제 존재하는 타임존이어야 함
        location (str): 지역명. 타임존이 모든 지명에 대응되지 않기 때문에 이후 llm 답변 생성에 사용됨
    """
    target_timezone = ZoneInfo(timezone)
    now = datetime.now(target_timezone).strftime("%Y-%m-%d %H:%M:%S")
    location_and_local_time = f"{timezone} ({location}) 현재시각 {now}"

    return location_and_local_time

class StockHistoryInput(BaseModel):
    ticker: str = Field(..., title="주식 코드", description="주식 코드 (예: TSLA)")
    period: str = Field(..., title="기간", description="주식 데이터 조회 기간 (예: 1d, 1mo, 1y)")

@mcp.tool
def get_yf_stock_history(stock_history_input: StockHistoryInput) -> str:
    """
    주식 종목의 가격 데이터를 조회하는 도구
    """
    stock = yf.Ticker(stock_history_input.ticker)
    history = stock.history(period=stock_history_input.period)
    history_md = history.to_markdown()

    return history_md


@mcp.tool
def get_web_search(query: str, search_period: str="w", region: str="kr-kr") -> str:
    """
    특정 지역과 기간을 설정하여 웹 검색을 수행합니다.
    사용자의 질문에 정확하게 답변할 수 있도록 query, search_period, region을 생성하여 도구를 호출합니다.

    Args:
        query: 검색어
        search_period: 검색 기간 (예: {'일간': 'd', '주간': 'w', '월간': 'm', '연간': 'y' 등})
        region: 검색 지역 코드 (예: {'한국': 'kr-kr', '미국': 'us-en', '일본': 'jp-jp' 등})
    
    Returns:
        검색된 결과 문자열
    """
    wrapper = DuckDuckGoSearchAPIWrapper(
        region=region,
        time=search_period
    )

    search = DuckDuckGoSearchResults(
        api_wrapper=wrapper,
        results_separator=";\n"
    )

    searched = search.invoke(query)
    return searched
    
if __name__ == "__main__":
    mcp.run(transport="http", port=8000) # HTTP

# https://modelcontextprotocol.io/docs/tools/inspector