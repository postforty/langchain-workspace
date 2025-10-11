"""메인 실행 파일"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from nike_crawler.config import ConfigManager
from nike_crawler.logger import setup_logger
from nike_crawler.naver_shopping import NaverShoppingCrawler


async def main():
    """메인 함수"""
    try:
        # 로깅 설정
        logger = setup_logger()
        logger.info("나이키 신발 크롤러 시작")
        
        # 설정 로드
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # 크롤러 실행
        async with NaverShoppingCrawler(config) as crawler:
            # 네이버 쇼핑 홈페이지 접근
            logger.info("네이버 쇼핑 홈페이지 접근 시도...")
            if await crawler.access_homepage():
                logger.info("홈페이지 접근 성공!")
                
                # 현재 URL과 제목 출력
                current_url = await crawler.get_current_url()
                page_title = await crawler.get_page_title()
                logger.info(f"현재 URL: {current_url}")
                logger.info(f"페이지 제목: {page_title}")
                
                # 나이키 신발 검색
                logger.info("나이키 신발 검색 시도...")
                if await crawler.search_nike_shoes():
                    logger.info("검색 성공!")
                    
                    # 검색 결과 URL 출력
                    search_url = await crawler.get_current_url()
                    logger.info(f"검색 결과 URL: {search_url}")
                else:
                    logger.error("검색 실패")
            else:
                logger.error("홈페이지 접근 실패")
                
    except Exception as e:
        logger.error(f"크롤링 중 오류 발생: {e}")
        return 1
        
    logger.info("크롤링 완료")
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)