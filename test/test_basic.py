"""기본 브라우저 테스트"""

import asyncio
from playwright.async_api import async_playwright


async def test_basic_browser():
    """기본 브라우저 기능 테스트"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 브라우저 창을 보이게 함
        page = await browser.new_page()
        
        try:
            # 간단한 사이트로 테스트
            print("Google 접근 테스트...")
            await page.goto("https://www.google.com")
            print(f"Google 접근 성공: {page.url}")
            
            # 네이버 메인 페이지 테스트
            print("네이버 메인 페이지 접근 테스트...")
            await page.goto("https://www.naver.com")
            print(f"네이버 접근 성공: {page.url}")
            
            # 네이버 쇼핑 테스트
            print("네이버 쇼핑 접근 테스트...")
            await page.goto("https://shopping.naver.com")
            print(f"네이버 쇼핑 접근 성공: {page.url}")
            
            # 페이지 제목 확인
            title = await page.title()
            print(f"페이지 제목: {title}")
            
            # 5초 대기
            await asyncio.sleep(5)
            
        except Exception as e:
            print(f"오류 발생: {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(test_basic_browser())
