import pytest
import numpy as np
from ai.recommendation.embedding_service import get_embedding_service


def test_embedding_service_dimensions_and_norm():
    service = get_embedding_service()
    assert service.vector_dimension > 0

    text = "Mysuru Dasara royal palace cultural heritage festival"
    vec = service.encode_text(text)

    assert isinstance(vec, np.ndarray)
    assert vec.shape == (service.vector_dimension,)
    assert vec.dtype == np.float32

    # Check L2 unit normalization (norm should be ~1.0)
    norm = np.linalg.norm(vec)
    assert pytest.approx(norm, abs=1e-3) == 1.0


def test_embedding_empty_text():
    service = get_embedding_service()
    vec = service.encode_text("")
    assert vec.shape == (service.vector_dimension,)
    assert np.all(vec == 0)


def test_embedding_batch_documents():
    service = get_embedding_service()
    docs = [
        "Hampi Utsav stone monuments and architecture",
        "Kambala buffalo mud race in coastal Mangaluru",
        "Bengaluru Karaga night floral procession"
    ]
    vecs = service.encode_documents(docs)
    assert vecs.shape == (3, service.vector_dimension)
    for i in range(3):
        norm = np.linalg.norm(vecs[i])
        assert pytest.approx(norm, abs=1e-3) == 1.0
