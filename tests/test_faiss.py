import os
import pytest
import numpy as np
from ai.recommendation.faiss_service import FAISSService
from ai.recommendation.embedding_service import get_embedding_service


def test_faiss_build_and_search(tmp_path):
    dim = 384
    service = FAISSService(vector_dimension=dim)

    # Mock index path to temp directory
    service.index_path = tmp_path / "test_faiss.bin"
    service.mapping_path = tmp_path / "test_mapping.json"
    service._reset_index()

    ids = ["fest-1", "fest-2", "fest-3"]
    # Generate random normalized 2D vectors
    v1 = np.random.randn(dim).astype(np.float32)
    v1 = v1 / np.linalg.norm(v1)

    v2 = np.random.randn(dim).astype(np.float32)
    v2 = v2 / np.linalg.norm(v2)

    v3 = np.random.randn(dim).astype(np.float32)
    v3 = v3 / np.linalg.norm(v3)

    vectors = np.vstack([v1, v2, v3])

    # Build index
    service.build_index(ids, vectors)
    assert service.get_total_vectors() == 3
    assert service.index_path.exists()
    assert service.mapping_path.exists()

    # Search with v1 query vector (exact match should score ~1.0)
    results = service.search(v1, top_k=2)
    assert len(results) == 2
    top_id, top_score = results[0]
    assert top_id == "fest-1"
    assert pytest.approx(top_score, abs=1e-2) == 1.0


def test_faiss_incremental_add_and_remove(tmp_path):
    dim = 384
    service = FAISSService(vector_dimension=dim)
    service.index_path = tmp_path / "test_faiss2.bin"
    service.mapping_path = tmp_path / "test_mapping2.json"
    service._reset_index()

    v1 = np.random.randn(dim).astype(np.float32)
    v1 = v1 / np.linalg.norm(v1)

    service.add_vector("fest-add-1", v1)
    assert service.get_total_vectors() == 1
    assert "fest-add-1" in service.id_mapping

    # Remove vector
    service.remove_vector("fest-add-1")
    assert service.get_total_vectors() == 0
    assert "fest-add-1" not in service.id_mapping
