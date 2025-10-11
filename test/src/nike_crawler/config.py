"""설정 관리 모듈"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """설정 관리 클래스"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        설정 관리자 초기화
        
        Args:
            config_path: 설정 파일 경로
        """
        self.config_path = Path(config_path)
        self.logger = logging.getLogger(__name__)
        self._config: Dict[str, Any] = {}
        
    def load_config(self) -> Dict[str, Any]:
        """
        설정 파일 로드
        
        Returns:
            Dict[str, Any]: 설정 딕셔너리
            
        Raises:
            FileNotFoundError: 설정 파일이 없을 때
            yaml.YAMLError: YAML 파싱 오류 시
        """
        try:
            if not self.config_path.exists():
                raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {self.config_path}")
                
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
                
            # 기본값 설정
            self._set_defaults()
            
            # 설정 유효성 검증
            self._validate_config()
            
            self.logger.info(f"설정 파일 로드 완료: {self.config_path}")
            return self._config
            
        except FileNotFoundError as e:
            self.logger.error(f"설정 파일 오류: {e}")
            raise
        except yaml.YAMLError as e:
            self.logger.error(f"YAML 파싱 오류: {e}")
            raise
        except Exception as e:
            self.logger.error(f"설정 로드 중 예상치 못한 오류: {e}")
            raise
            
    def _set_defaults(self) -> None:
        """기본값 설정"""
        defaults = {
            'crawling': {
                'max_pages': 10,
                'delay_between_requests': 2000,
                'timeout': 30000,
                'retry_count': 3,
                'headless': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            'output': {
                'format': ['csv', 'json'],
                'directory': './output',
                'include_images': True,
                'filename_prefix': 'nike_shoes'
            },
            'filters': {
                'min_price': 0,
                'max_price': 1000000,
                'min_rating': 0,
                'categories': ['운동화', '스니커즈'],
                'brands': ['나이키']
            },
            'logging': {
                'level': 'INFO',
                'file': './logs/crawler.log',
                'max_size': '10MB',
                'backup_count': 5
            },
            'search': {
                'keyword': '나이키 신발',
                'sort_by': 'rel',
                'page_size': 40
            }
        }
        
        # 기본값 병합
        for section, values in defaults.items():
            if section not in self._config:
                self._config[section] = values
            else:
                for key, value in values.items():
                    if key not in self._config[section]:
                        self._config[section][key] = value
                        
    def _validate_config(self) -> None:
        """설정 유효성 검증"""
        required_sections = ['crawling', 'output', 'search']
        
        for section in required_sections:
            if section not in self._config:
                raise ValueError(f"필수 설정 섹션이 없습니다: {section}")
                
        # 크롤링 설정 검증
        crawling = self._config['crawling']
        if not isinstance(crawling.get('max_pages'), int) or crawling['max_pages'] <= 0:
            raise ValueError("max_pages는 양의 정수여야 합니다")
            
        if not isinstance(crawling.get('timeout'), int) or crawling['timeout'] <= 0:
            raise ValueError("timeout은 양의 정수여야 합니다")
            
        # 출력 설정 검증
        output = self._config['output']
        if not isinstance(output.get('format'), list) or not output['format']:
            raise ValueError("output.format은 비어있지 않은 리스트여야 합니다")
            
        # 검색 설정 검증
        search = self._config['search']
        if not search.get('keyword'):
            raise ValueError("search.keyword는 필수입니다")
            
    def get(self, key: str, default: Any = None) -> Any:
        """
        설정값 조회
        
        Args:
            key: 설정 키 (예: 'crawling.timeout')
            default: 기본값
            
        Returns:
            Any: 설정값
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
            
    def save_config(self, config: Dict[str, Any] = None) -> None:
        """
        설정 파일 저장
        
        Args:
            config: 저장할 설정 (None이면 현재 설정 저장)
        """
        if config is not None:
            self._config = config
            
        try:
            # 디렉토리 생성
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
                
            self.logger.info(f"설정 파일 저장 완료: {self.config_path}")
            
        except Exception as e:
            self.logger.error(f"설정 파일 저장 중 오류: {e}")
            raise
