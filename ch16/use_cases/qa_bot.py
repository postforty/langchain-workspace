from use_cases.interfaces import IDocumentRepository, IQAService

class QABotUseCase:
    """RAG 기반 질의응답 비즈니스 흐름 제어"""
    
    def __init__(self, doc_repo: IDocumentRepository, qa_service: IQAService):
        self.doc_repo = doc_repo
        self.qa_service = qa_service
        
    def execute(self, query: str) -> str:
        # 1. 쿼리와 연관된 문서를 벡터 DB에서 검색 (Top-K)
        chunks = self.doc_repo.search_similar(query, top_k=3)
        if not chunks:
            return "문맥에서 관련된 정보를 찾을 수 없습니다."
            
        # 2. 청크 텍스트 병합 (컨텍스트 구성)
        context = "\n\n".join(chunk.text for chunk in chunks)
        
        # 3. LLM을 통해 답변 생성
        return self.qa_service.answer_question(query, context)
