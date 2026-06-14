import random
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

from domain.models import DocumentChunk
from use_cases.interfaces import IDocumentRepository

class FAISSRepository(IDocumentRepository):
    """Ollama bge-m3 임베딩과 FAISS를 활용한 벡터 DB 어댑터 구현체"""
    
    def __init__(self, model_name: str = "bge-m3"):
        self.embeddings = OllamaEmbeddings(model=model_name)
        self.vectorstore = None
        self.indexed_chunks: List[DocumentChunk] = []

    def index_documents(self, chunks: List[DocumentChunk]) -> None:
        """DocumentChunk 리스트를 받아 FAISS 인덱스를 생성합니다."""
        self.indexed_chunks = chunks
        
        # 도메인 모델을 LangChain Document 객체로 변환
        docs = [
            Document(page_content=chunk.text, metadata=chunk.metadata)
            for chunk in chunks
        ]
        
        # 문서와 임베딩을 이용해 벡터 저장소 구축
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)

    def search_similar(self, query: str, top_k: int = 3) -> List[DocumentChunk]:
        """쿼리와 가장 유사한 문서를 반환 (방어 로직 2, 3 포함)"""
        if not self.vectorstore:
            return []
            
        # 방어 로직 2: 연관된 여러 조각(Top-K)을 합쳐서 리턴하기 위해 K개 조회
        # 추후 Parent Document Retriever 등 정밀 검색으로 고도화 가능 (방어 로직 3)
        docs = self.vectorstore.similarity_search(query, k=top_k)
        
        results = []
        for doc in docs:
            chunk = DocumentChunk(text=doc.page_content, metadata=doc.metadata)
            results.append(chunk)
            
        return results

    def get_random_chunks(self, count: int = 1) -> List[DocumentChunk]:
        """무작위 문서 청크를 추출 (퀴즈 출제용 등)"""
        if not self.indexed_chunks:
            return []
        
        sample_size = min(count, len(self.indexed_chunks))
        return random.sample(self.indexed_chunks, sample_size)
