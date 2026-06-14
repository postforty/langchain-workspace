import pytest
from unittest.mock import MagicMock
from domain.models import DocumentChunk

# This import will fail initially (Red phase)
from interface_adapters.repositories.faiss_repo import FAISSRepository

def test_index_documents(mocker):
    # Mock FAISS and OllamaEmbeddings
    mock_faiss = mocker.patch("interface_adapters.repositories.faiss_repo.FAISS")
    mock_embeddings = mocker.patch("interface_adapters.repositories.faiss_repo.OllamaEmbeddings")
    
    repo = FAISSRepository()
    chunks = [
        DocumentChunk(text="Chunk 1", metadata={"source": "test.pdf", "start_index": 0, "end_index": 100}),
        DocumentChunk(text="Chunk 2", metadata={"source": "test.pdf", "start_index": 50, "end_index": 150}),
    ]
    
    repo.index_documents(chunks)
    
    # Assert FAISS.from_documents was called
    assert mock_faiss.from_documents.called
    assert repo.vectorstore is not None

def test_search_similar(mocker):
    repo = FAISSRepository()
    repo.vectorstore = mocker.MagicMock()
    
    # Mock Document return from FAISS
    mock_doc1 = mocker.MagicMock()
    mock_doc1.page_content = "Similar text 1"
    mock_doc1.metadata = {"source": "test.pdf"}
    
    mock_doc2 = mocker.MagicMock()
    mock_doc2.page_content = "Similar text 2"
    mock_doc2.metadata = {"source": "test.pdf"}
    
    repo.vectorstore.similarity_search.return_value = [mock_doc1, mock_doc2]
    
    results = repo.search_similar("query", top_k=2)
    
    # Assert defense logic 2 (Multi-Chunk Top-K Return)
    assert len(results) == 2
    assert results[0].text == "Similar text 1"
    assert results[1].text == "Similar text 2"
    repo.vectorstore.similarity_search.assert_called_with("query", k=2)

def test_get_random_chunks(mocker):
    repo = FAISSRepository()
    
    # Set internal chunks state to simulate already indexed documents
    repo.indexed_chunks = [
        DocumentChunk(text="Random text 1", metadata={"source": "test.pdf"}),
        DocumentChunk(text="Random text 2", metadata={"source": "test.pdf"}),
        DocumentChunk(text="Random text 3", metadata={"source": "test.pdf"})
    ]
    
    results = repo.get_random_chunks(count=2)
    
    assert len(results) == 2
    assert results[0].text in ["Random text 1", "Random text 2", "Random text 3"]
