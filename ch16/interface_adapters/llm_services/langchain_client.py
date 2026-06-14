from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from domain.models import Question
from use_cases.interfaces import IQuestionGenerator, IQAService

class LangChainGeminiClient(IQuestionGenerator, IQAService):
    """Gemini LLM을 이용하여 문제 출제 및 질의응답을 수행하는 어댑터 클래스"""
    
    def __init__(self, model_name: str = "gemini-3.1-flash-lite"):
        # 모델 초기화 (temperature를 낮게 설정하여 환각 방지)
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.1)
        
        # [방어 로직 4] 엄격한 프롬프트 제어 - 문제 출제용
        self.question_prompt = PromptTemplate.from_template(
            "다음 [문맥]을 읽고, 이 문맥에 기반하여 학습용 4지선다 문제를 하나 출제하세요.\n\n"
            "[제약 사항]\n"
            "1. 문맥에 없는 내용은 절대로 문제에 포함하지 마세요.\n"
            "2. 보기는 반드시 4개여야 합니다.\n"
            "3. 정답 인덱스는 0, 1, 2, 3 중 하나여야 합니다.\n\n"
            "[문맥]\n{context}"
        )
        
        # Pydantic 모델을 활용한 구조화된 출력 강제
        structured_llm = self.llm.with_structured_output(Question)
        self._question_chain = self.question_prompt | structured_llm
        
        # [방어 로직 4] 엄격한 프롬프트 제어 - RAG 질의응답용
        self.qa_prompt = PromptTemplate.from_template(
            "다음 [참고 문맥]을 바탕으로 사용자의 [질문]에 답변하세요.\n\n"
            "[제약 사항]\n"
            "1. 참고 문맥에 있는 정보만 사용하여 답변하세요.\n"
            "2. 참고 문맥으로 전혀 알 수 없는 내용이라면, '문맥에서 찾을 수 없습니다'라고만 답변하세요.\n\n"
            "[참고 문맥]\n{context}\n\n"
            "[질문]\n{query}"
        )
        
        self._qa_chain = self.qa_prompt | self.llm | StrOutputParser()

    def generate_question_from_context(self, context: str) -> Optional[Question]:
        """제공된 컨텍스트(문맥)를 바탕으로 문제를 생성"""
        try:
            # Chain 실행 (구조화된 출력으로 인해 자동 Pydantic 객체 파싱됨)
            result = self._question_chain.invoke({"context": context})
            return result
        except Exception:
            # 파싱 실패나 모델 응답 오류 시 None 반환
            return None

    def answer_question(self, query: str, context: str) -> str:
        """제공된 컨텍스트를 바탕으로 사용자 질문에 답변"""
        response = self._qa_chain.invoke({"query": query, "context": context})
        return response
