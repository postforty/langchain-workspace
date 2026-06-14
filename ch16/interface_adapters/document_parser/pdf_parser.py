import fitz  # PyMuPDF
from typing import List
from domain.models import DocumentChunk

class PDFParser:
    """PDF 문서를 읽고 Chunk 단위로 분할하는 어댑터 클래스"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        # [방어 로직 1] 문맥 단절 방지를 위한 Chunk Overlap 설정
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def parse_and_chunk(self, file_bytes: bytes, file_name: str) -> List[DocumentChunk]:
        """PDF 바이트 데이터를 읽어서 오버랩이 적용된 DocumentChunk 리스트로 반환"""
        text = self._extract_text_from_pdf(file_bytes)
        return self._split_text_with_overlap(text, file_name)
        
    def _extract_text_from_pdf(self, file_bytes: bytes) -> str:
        text = ""
        # fitz (PyMuPDF)를 사용하여 메모리 상의 바이트 데이터로부터 텍스트 추출
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text() + "\n"
        return text

    def _split_text_with_overlap(self, text: str, file_name: str) -> List[DocumentChunk]:
        """기본적인 문자 단위 Chunk 분할 로직 (Overlap 적용)"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            chunk = DocumentChunk(
                text=chunk_text,
                metadata={"source": file_name, "start_index": start, "end_index": end}
            )
            chunks.append(chunk)
            
            # 다음 청크 시작 위치를 overlap 만큼 뒤로 당김
            start += (self.chunk_size - self.chunk_overlap)
            
        return chunks
