from typing import List, Optional
from pydantic import BaseModel, Field


class LocationInput(BaseModel):
    city: Optional[str] = Field(default=None, description="City or place name")
    latitude: Optional[float] = Field(default=None, description="Latitude coordinate")
    longitude: Optional[float] = Field(default=None, description="Longitude coordinate")


class TouristPreferenceInput(BaseModel):
    interests: List[str] = Field(default_factory=list, description="List of tourist interests (e.g. folk, food, heritage, music)")
    query: Optional[str] = Field(default=None, description="Natural language preference query")
    location: Optional[LocationInput] = Field(default=None, description="Tourist current or intended travel location")
    start_date: Optional[str] = Field(default=None, description="Travel start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(default=None, description="Travel end date (YYYY-MM-DD)")
    language: str = Field(default="en", description="Preferred response language code (en, kn, hi)")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of recommendations to return")


class RecommendationItem(BaseModel):
    festival_id: str
    festival_name: str
    category: str
    description: str
    match_score: int  # 0 to 100
    match_reason: str
    explanation_signals: List[str] = Field(default_factory=list)
    location: str
    district: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    distance_km: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    date_relevance: float = 0.0
    semantic_score: float = 0.0
    location_score: float = 0.0
    category_score: float = 0.0
    image_url: Optional[str] = None


class RecommendationResponse(BaseModel):
    success: bool = True
    language: str = "en"
    total_found: int = 0
    recommendations: List[RecommendationItem] = Field(default_factory=list)
    algorithm_info: str = "SentenceTransformers + FAISS + Haversine Hybrid Ranking v1.0"
    vector_dimension: int = 384
    message: Optional[str] = None


class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to translate")
    source_language: Optional[str] = Field(default=None, description="Source language code (auto-detected if omitted)")
    target_language: str = Field(..., description="Target language code (en, kn, hi)")


class TranslationResponse(BaseModel):
    success: bool = True
    source_language: str
    target_language: str
    translated_text: str
    cached: bool = False


class BatchTranslationRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, description="List of text strings to translate")
    source_language: Optional[str] = Field(default=None)
    target_language: str = Field(...)


class BatchTranslationResponse(BaseModel):
    success: bool = True
    source_language: str
    target_language: str
    translated_texts: List[str]


class FestivalTranslationResponse(BaseModel):
    success: bool = True
    festival_id: str
    language: str
    name: str
    category: str
    description: str
    history: Optional[str] = None
    cultural_significance: Optional[str] = None
    activities: List[str] = Field(default_factory=list)
    food: List[str] = Field(default_factory=list)
    tourist_info: Optional[str] = None


class IndexStatusResponse(BaseModel):
    success: bool = True
    total_indexed_vectors: int
    faiss_index_path: str
    last_updated: Optional[str] = None
    message: Optional[str] = None
