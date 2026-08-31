import pytest
from database.models import Festival
from ai.models.schemas import TouristPreferenceInput, LocationInput
from ai.recommendation.ranking_service import RankingService, haversine_distance_km


def test_haversine_distance():
    # Bengaluru (12.9716, 77.5946) to Mysuru (12.3052, 76.6552) ~ 130-145 km
    dist = haversine_distance_km(12.9716, 77.5946, 12.3052, 76.6552)
    assert 120.0 <= dist <= 150.0


def test_ranking_service_scoring():
    ranker = RankingService(
        semantic_weight=0.50,
        location_weight=0.20,
        date_weight=0.20,
        category_weight=0.10
    )

    fest = Festival(
        id="test-fest-1",
        name="Mysuru Dasara",
        category="Heritage, Royal, Cultural",
        description="Palace illumination and jumboo savari",
        location="Mysore Palace",
        district="Mysuru",
        state="Karnataka",
        latitude=12.3052,
        longitude=76.6552,
        start_date="2026-10-01",
        end_date="2026-10-10",
        tags='["heritage", "folk", "food", "palace"]'
    )

    prefs = TouristPreferenceInput(
        interests=["heritage", "folk", "food"],
        location=LocationInput(city="Bengaluru", latitude=12.9716, longitude=77.5946),
        start_date="2026-10-01",
        end_date="2026-10-05",
        language="en"
    )

    result = ranker.rank_festival(
        semantic_score=0.90,
        festival=fest,
        preferences=prefs
    )

    assert "match_score" in result
    assert 0 <= result["match_score"] <= 100
    assert result["match_score"] > 80  # High match expected for perfect date & high semantic similarity
    assert result["date_score"] == 1.0  # Perfect overlap
    assert result["distance_km"] is not None
    assert 120.0 <= result["distance_km"] <= 150.0
