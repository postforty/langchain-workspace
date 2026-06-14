import pytest
from interface_adapters.document_parser.pdf_parser import PDFParser

def test_pdf_parser_chunking(mocker):
    # Mocking fitz.open to avoid needing an actual PDF file
    mock_doc = mocker.MagicMock()
    mock_page1 = mocker.MagicMock()
    mock_page1.get_text.return_value = "A" * 500
    mock_page2 = mocker.MagicMock()
    mock_page2.get_text.return_value = "B" * 500
    
    # Doc acts like an iterator of pages
    mock_doc.__enter__.return_value = [mock_page1, mock_page2]
    
    mock_fitz_open = mocker.patch("interface_adapters.document_parser.pdf_parser.fitz.open", return_value=mock_doc)
    
    # Create parser with specific chunk_size and chunk_overlap for testing
    parser = PDFParser(chunk_size=400, chunk_overlap=100)
    
    chunks = parser.parse_and_chunk(b"dummy_bytes", "test.pdf")
    
    # Total text is 500 A's + \n + 500 B's + \n = 1002 chars
    # chunk 1: 0 ~ 400
    # chunk 2: 300 ~ 700 (overlap 100)
    # chunk 3: 600 ~ 1000
    # chunk 4: 900 ~ 1300
    
    assert mock_fitz_open.called
    assert len(chunks) == 4
    assert chunks[0].metadata["start_index"] == 0
    assert chunks[0].metadata["end_index"] == 400
    assert chunks[0].metadata["source"] == "test.pdf"
    
    assert chunks[1].metadata["start_index"] == 300
    assert chunks[1].metadata["end_index"] == 700
