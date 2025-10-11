"""로깅 설정 모듈"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "nike_crawler",
    level: str = "INFO",
    log_file: Optional[str] = None,
    max_size: str = "10MB",
    backup_count: int = 5
) -> logging.Logger:
    """
    로거 설정
    
    Args:
        name: 로거 이름
        level: 로그 레벨
        log_file: 로그 파일 경로
        max_size: 로그 파일 최대 크기
        backup_count: 백업 파일 개수
        
    Returns:
        logging.Logger: 설정된 로거
    """
    logger = logging.getLogger(name)
    
    # 이미 핸들러가 설정되어 있으면 기존 로거 반환
    if logger.handlers:
        return logger
        
    # 로그 레벨 설정
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 포맷터 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 파일 핸들러 설정 (로그 파일이 지정된 경우)
    if log_file:
        log_path = Path(log_file)
        
        # 로그 디렉토리 생성
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 파일 크기 파싱
        size_bytes = _parse_size(max_size)
        
        # 로테이팅 파일 핸들러 설정
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=size_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def _parse_size(size_str: str) -> int:
    """
    크기 문자열을 바이트로 변환
    
    Args:
        size_str: 크기 문자열 (예: "10MB", "1GB")
        
    Returns:
        int: 바이트 크기
    """
    size_str = size_str.upper().strip()
    
    if size_str.endswith('KB'):
        return int(size_str[:-2]) * 1024
    elif size_str.endswith('MB'):
        return int(size_str[:-2]) * 1024 * 1024
    elif size_str.endswith('GB'):
        return int(size_str[:-2]) * 1024 * 1024 * 1024
    else:
        # 기본값: MB로 간주
        return int(size_str) * 1024 * 1024


class CrawlerLogger:
    """크롤러 전용 로거 클래스"""
    
    def __init__(self, name: str = "nike_crawler"):
        self.logger = setup_logger(name)
        
    def info(self, message: str) -> None:
        """정보 로그"""
        self.logger.info(message)
        
    def warning(self, message: str) -> None:
        """경고 로그"""
        self.logger.warning(message)
        
    def error(self, message: str) -> None:
        """오류 로그"""
        self.logger.error(message)
        
    def debug(self, message: str) -> None:
        """디버그 로그"""
        self.logger.debug(message)
        
    def critical(self, message: str) -> None:
        """치명적 오류 로그"""
        self.logger.critical(message)
