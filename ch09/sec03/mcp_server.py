from fastmcp import FastMCP
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field
import yfinance as yf
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def get_current_time(timezone: str, location: str) -> str:
    """ 현재 시각을 반환하는 함수

    Args:
        timezone: 타임존 (예: 'Asia/Seoul') 실제 존재하는 타임존이어야 함
        location: 지역명, 타임존이 모든 지명에 대응되지 않기 때문에 이후 LLM 답변 생성에 사용됨
    """
    target_timezone = ZoneInfo(timezone)
    now = datetime.now(tz=target_timezone).strftime("%Y-%m-%d %H:%M:%S")
    location_and_local_time = f"{timezone} ({location}) 현재시각 {now}"
    return location_and_local_time

class StockHistoryInput(BaseModel):
    ticker: str = Field(..., title="주식 코드", description="주식 코드 (예: TSLA)")
    period: str = Field(..., title="기간", description="주식 데이터 조회 기간 (예: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)")

@mcp.tool
def get_yf_stock_history(stock_history_input: StockHistoryInput) -> str:
    """주식 종목의 가격 데이터를 조회하는 함수"""
    stock = yf.Ticker(stock_history_input.ticker)
    history = stock.history(period=stock_history_input.period)
    return history.to_markdown()

@mcp.tool
def get_web_search(query: str, search_period: str='w', region: str='kr-kr') -> str:
    """특정 지역과 기간을 설정하여 웹 검색을 수행합니다.
    
    Args:
        query: 검색어
        search_period: 검색 기간. 'd'(일간), 'w'(주간), 'm'(월간), 'y'(연간) 중 선택
        region: 검색 지역 코드. 한국('kr-kr'), 미국('us-en'), 일본('jp-jp'), 영국('uk-en') 등
    
    Returns:
        문자열(str)로된 검색 결과 리스트
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

if __name__ == "__main__":
    mcp.run()