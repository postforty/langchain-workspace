"""네이버 쇼핑 크롤링 모듈"""

import asyncio
import logging
from typing import Dict, List, Optional
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError


class NaverShoppingCrawler:
    """네이버 쇼핑 크롤러 클래스"""
    
    def __init__(self, config: Dict):
        """
        크롤러 초기화
        
        Args:
            config: 설정 딕셔너리
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
        # 설정값 추출
        self.timeout = config.get('crawling', {}).get('timeout', 30000)
        self.retry_count = config.get('crawling', {}).get('retry_count', 3)
        self.headless = config.get('crawling', {}).get('headless', True)
        self.user_agent = config.get('crawling', {}).get('user_agent', '')
        self.delay = config.get('crawling', {}).get('delay_between_requests', 2000)
        
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        await self.start_browser()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        await self.close_browser()
        
    async def start_browser(self) -> None:
        """
        브라우저 인스턴스 생성 및 시작
        
        Raises:
            Exception: 브라우저 시작 실패 시
        """
        try:
            self.logger.info("브라우저 인스턴스 생성 중...")
            
            self.playwright = await async_playwright().start()
            
            # 브라우저 옵션 설정 (단순화)
            browser_options = {
                'headless': self.headless,
                'args': [
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ]
            }
            
            self.browser = await self.playwright.chromium.launch(**browser_options)
            
            # 새 페이지 생성
            context_options = {
                'user_agent': self.user_agent,
                'viewport': {'width': 1920, 'height': 1080},
                'locale': 'ko-KR',
                'timezone_id': 'Asia/Seoul'
            }
            
            context = await self.browser.new_context(**context_options)
            self.page = await context.new_page()
            
            # 봇 탐지 우회를 위한 스크립트 추가
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            self.logger.info("브라우저 인스턴스 생성 완료")
            
        except Exception as e:
            self.logger.error(f"브라우저 시작 실패: {e}")
            raise
            
    async def close_browser(self) -> None:
        """브라우저 인스턴스 종료"""
        try:
            if self.browser:
                await self.browser.close()
                self.logger.info("브라우저 종료 완료")
        except Exception as e:
            self.logger.error(f"브라우저 종료 중 오류: {e}")
        finally:
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
                
    async def access_homepage(self) -> bool:
        """
        네이버 쇼핑 홈페이지 접근
        
        Returns:
            bool: 접근 성공 여부
        """
        url = "https://shopping.naver.com"
        
        for attempt in range(self.retry_count):
            try:
                self.logger.info(f"네이버 쇼핑 홈페이지 접근 시도 {attempt + 1}/{self.retry_count}")
                
                # 페이지 이동 (더 관대한 옵션 사용)
                response = await self.page.goto(
                    url, 
                    timeout=self.timeout,
                    wait_until="domcontentloaded"  # networkidle 대신 domcontentloaded 사용
                )
                
                # 응답 상태 확인 (더 유연하게)
                if response:
                    self.logger.info(f"HTTP 응답 상태: {response.status}")
                    if response.status in [200, 301, 302]:  # 리다이렉트도 허용
                        # 페이지 로딩 대기
                        await self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                        
                        # JavaScript 렌더링 완료 확인
                        await self._wait_for_js_rendering()
                        
                        self.logger.info("네이버 쇼핑 홈페이지 접근 성공")
                        return True
                    else:
                        self.logger.warning(f"HTTP 응답 오류: {response.status}")
                else:
                    self.logger.warning("응답 객체가 None입니다")
                    
            except PlaywrightTimeoutError:
                self.logger.warning(f"페이지 로딩 타임아웃 (시도 {attempt + 1}/{self.retry_count})")
            except Exception as e:
                self.logger.error(f"홈페이지 접근 실패 (시도 {attempt + 1}/{self.retry_count}): {e}")
                
            # 재시도 전 대기
            if attempt < self.retry_count - 1:
                await asyncio.sleep(2 ** attempt)  # 지수 백오프
                
        self.logger.error("네이버 쇼핑 홈페이지 접근 최종 실패")
        return False
        
    async def _wait_for_js_rendering(self) -> None:
        """
        JavaScript 렌더링 완료 대기
        
        Raises:
            PlaywrightTimeoutError: 렌더링 완료 타임아웃 시
        """
        try:
            # 주요 요소들이 로드될 때까지 대기
            selectors_to_wait = [
                'input[placeholder*="검색"]',  # 검색창
                '.gnb_my',  # 네비게이션
                '.shopping_header'  # 헤더
            ]
            
            for selector in selectors_to_wait:
                try:
                    await self.page.wait_for_selector(selector, timeout=10000)
                except PlaywrightTimeoutError:
                    self.logger.warning(f"선택자 {selector} 로딩 타임아웃")
                    
            # 추가 대기 시간 (동적 콘텐츠 로딩)
            await asyncio.sleep(2)
            
        except Exception as e:
            self.logger.error(f"JavaScript 렌더링 대기 중 오류: {e}")
            raise
            
    async def search_nike_shoes(self) -> bool:
        """
        나이키 신발 검색 실행
        
        Returns:
            bool: 검색 성공 여부
        """
        keyword = self.config.get('search', {}).get('keyword', '나이키 신발')
        
        for attempt in range(self.retry_count):
            try:
                self.logger.info(f"나이키 신발 검색 시도 {attempt + 1}/{self.retry_count}")
                
                # 검색창 요소 식별 및 클릭
                search_selectors = [
                    'input[placeholder*="검색"]',
                    'input[name="query"]',
                    '.search_input',
                    '#query'
                ]
                
                search_input = None
                for selector in search_selectors:
                    try:
                        search_input = self.page.locator(selector).first
                        if await search_input.is_visible():
                            break
                    except:
                        continue
                        
                if not search_input:
                    raise Exception("검색창을 찾을 수 없습니다")
                    
                # 검색창 클릭 및 검색어 입력
                await search_input.click()
                await search_input.fill(keyword)
                
                # 검색 실행 (Enter 키 또는 검색 버튼 클릭)
                try:
                    await search_input.press("Enter")
                except:
                    # 검색 버튼 클릭 시도
                    search_button_selectors = [
                        'button[type="submit"]',
                        '.search_btn',
                        '.btn_search'
                    ]
                    
                    for btn_selector in search_button_selectors:
                        try:
                            search_btn = self.page.locator(btn_selector).first
                            if await search_btn.is_visible():
                                await search_btn.click()
                                break
                        except:
                            continue
                
                # 검색 결과 페이지 로딩 대기
                await self.page.wait_for_load_state("networkidle", timeout=self.timeout)
                
                # 검색 결과 확인
                if await self._verify_search_results():
                    self.logger.info("나이키 신발 검색 성공")
                    return True
                else:
                    self.logger.warning("검색 결과가 없거나 예상과 다름")
                    
            except Exception as e:
                self.logger.error(f"검색 실패 (시도 {attempt + 1}/{self.retry_count}): {e}")
                
            # 재시도 전 대기
            if attempt < self.retry_count - 1:
                await asyncio.sleep(2 ** attempt)
                
        self.logger.error("나이키 신발 검색 최종 실패")
        return False
        
    async def _verify_search_results(self) -> bool:
        """
        검색 결과 유효성 검증
        
        Returns:
            bool: 검색 결과 유효성
        """
        try:
            # 검색 결과 컨테이너 확인
            result_selectors = [
                '.product_list',
                '.search_product_list',
                '.product_item',
                '[data-testid="product-list"]'
            ]
            
            for selector in result_selectors:
                try:
                    element = self.page.locator(selector).first
                    if await element.is_visible():
                        # 상품이 있는지 확인
                        products = await element.locator('.product_item, .product_list_item').count()
                        if products > 0:
                            self.logger.info(f"검색 결과 확인: {products}개 상품 발견")
                            return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            self.logger.error(f"검색 결과 검증 중 오류: {e}")
            return False
            
    async def get_current_url(self) -> str:
        """현재 페이지 URL 반환"""
        return self.page.url if self.page else ""
        
    async def get_page_title(self) -> str:
        """현재 페이지 제목 반환"""
        return await self.page.title() if self.page else ""
