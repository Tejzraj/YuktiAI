import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from ai.models.schemas import TouristPreferenceInput, RecommendationResponse
from ai.recommendation.recommendation_service import RecommendationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["AI Recommendation Engine"])


@router.post(
    "/recommendations",
    response_model=RecommendationResponse,
    summary="Get AI Cultural Experience Recommendations",
    description="""
    Generates personalized Karnataka cultural festival and event recommendations using:
    - Sentence Transformer semantic query vector encoding
    - FAISS vector search
    - Dynamic database fetching of published cultural events
    - Hybrid Ranking Engine (Semantic + Haversine Location + Travel Date Overlap + Interest Category)
    - Signal-backed match explanation generator ("Why this festival matches you")
    - Multilingual localization support (English, Kannada, Hindi)
    """
)
def get_cultural_recommendations(
    preferences: TouristPreferenceInput,
    db: Session = Depends(get_db)
):
    try:
        service = RecommendationService(db)
        response = service.get_recommendations(preferences)
        return response
    except Exception as e:
        logger.error(f"Error executing recommendation pipeline: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while generating recommendations: {str(e)}"
        )
