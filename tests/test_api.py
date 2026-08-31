import pytest
from fastapi.testclient import TestClient
from api.main import app
from database.connection import Base, engine, SessionLocal
from database.seed import seed_database
from ai.recommendation.index_manager import IndexManager

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_test_db_and_index():
    Base.metadata.create_all(bind=engine)
    seed_database()
    db = SessionLocal()
    mgr = IndexManager(db)
    mgr.rebuild_index()
    db.close()


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_recommendation_api():
    payload = {
        "interests": ["folk", "food", "heritage"],
        "location": {
            "city": "Bengaluru",
            "latitude": 12.9716,
            "longitude": 77.5946
        },
        "start_date": "2026-10-01",
        "end_date": "2026-10-10",
        "language": "en",
        "limit": 5
    }
    response = client.post("/api/ai/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_found"] > 0
    assert len(data["recommendations"]) <= 5

    rec = data["recommendations"][0]
    assert "festival_id" in rec
    assert "match_score" in rec
    assert "match_reason" in rec
    assert rec["match_score"] > 0


def test_multilingual_recommendation_api():
    payload = {
        "interests": ["folk", "food"],
        "language": "kn",
        "limit": 3
    }
    response = client.post("/api/ai/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["language"] == "kn"


def test_single_translation_api():
    payload = {
        "text": "Traditional cultural festival",
        "target_language": "kn"
    }
    response = client.post("/api/translate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["target_language"] == "kn"
    assert len(data["translated_text"]) > 0


def test_faiss_index_status_api():
    response = client.get("/api/ai/index/status")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["total_indexed_vectors"] > 0
