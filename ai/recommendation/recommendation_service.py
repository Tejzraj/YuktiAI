import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from config import settings
from database.models import Festival
from ai.models.schemas import TouristPreferenceInput, RecommendationItem, RecommendationResponse
from ai.recommendation.embedding_service import get_embedding_service
from ai.recommendation.faiss_service import FAISSService
from ai.recommendation.ranking_service import RankingService
from ai.recommendation.explanation_service import ExplanationService

logger = logging.getLogger(__name__)


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = get_embedding_service()
        self.faiss_service = FAISSService(vector_dimension=self.embedding_service.vector_dimension)
        self.ranking_service = RankingService()

    def get_recommendations(self, preferences: TouristPreferenceInput) -> RecommendationResponse:
        """
        Main recommendation pipeline:
        1. Formulate semantic query string
        2. Encode query to vector
        3. Perform FAISS vector search
        4. Fetch published festival candidates from DB
        5. Apply hybrid ranking
        6. Generate explanations
        7. Format & translate response if requested
        """
        # 1. Build semantic query text
        query_parts = []
        if preferences.query and preferences.query.strip():
            query_parts.append(preferences.query.strip())
        if preferences.interests:
            query_parts.append(f"Interests: {', '.join(preferences.interests)}")
        if preferences.location and preferences.location.city:
            query_parts.append(f"Location preference: {preferences.location.city}")

        full_query_text = " ".join(query_parts) if query_parts else "Karnataka cultural heritage festivals folk food traditions"

        # 2. Encode query vector
        query_vector = self.embedding_service.encode_text(full_query_text)

        # 3. FAISS candidate search
        top_k = max(settings.FAISS_TOP_K, preferences.limit * 2)
        candidate_matches = self.faiss_service.search(query_vector, top_k=top_k)

        if not candidate_matches:
            # Fallback: if FAISS is empty, query database directly for published festivals
            logger.info("FAISS returned 0 candidate matches. Fetching directly from DB.")
            db_festivals = self.db.query(Festival).filter(
                Festival.is_published == True,
                Festival.verification_status == "verified"
            ).limit(preferences.limit).all()

            candidate_matches = [(f.id, 0.5) for f in db_festivals]

        # 4. Fetch DB records & map FAISS similarity scores
        fest_id_map = {fid: sim for fid, sim in candidate_matches}
        candidate_ids = list(fest_id_map.keys())

        festivals = self.db.query(Festival).filter(
            Festival.id.in_(candidate_ids),
            Festival.is_published == True,
            Festival.verification_status == "verified"
        ).all()

        if not festivals:
            return RecommendationResponse(
                success=True,
                language=preferences.language,
                total_found=0,
                recommendations=[],
                message="No matching cultural experiences were found."
            )

        # 5. Apply Hybrid Ranking & Explanation
        ranked_items: List[RecommendationItem] = []

        for festival in festivals:
            sem_score = fest_id_map.get(festival.id, 0.5)

            # Compute hybrid score
            scores = self.ranking_service.rank_festival(
                semantic_score=sem_score,
                festival=festival,
                preferences=preferences
            )

            # Generate explanation
            explanation = ExplanationService.generate_explanation(
                festival=festival,
                scores=scores,
                preferences=preferences
            )

            item = RecommendationItem(
                festival_id=festival.id,
                festival_name=festival.name,
                category=festival.category,
                description=festival.description,
                match_score=scores["match_score"],
                match_reason=explanation["match_reason"],
                explanation_signals=explanation["explanation_signals"],
                location=festival.location,
                district=festival.district,
                latitude=festival.latitude,
                longitude=festival.longitude,
                distance_km=scores["distance_km"],
                start_date=festival.start_date,
                end_date=festival.end_date,
                date_relevance=scores["date_score"],
                semantic_score=scores["semantic_score"],
                location_score=scores["location_score"],
                category_score=scores["category_score"],
                image_url=festival.image_url
            )
            ranked_items.append(item)

        # 6. Sort by match_score descending
        ranked_items.sort(key=lambda x: x.match_score, reverse=True)
        top_recommendations = ranked_items[:preferences.limit]

        # 7. Translate output if language is 'kn' or 'hi'
        target_lang = preferences.language.lower()
        if target_lang in ("kn", "hi"):
            top_recommendations = self._translate_recommendations(top_recommendations, target_lang)

        return RecommendationResponse(
            success=True,
            language=target_lang,
            total_found=len(top_recommendations),
            recommendations=top_recommendations,
            vector_dimension=self.embedding_service.vector_dimension
        )

    def _translate_recommendations(
        self,
        recommendations: List[RecommendationItem],
        target_language: str
    ) -> List[RecommendationItem]:
        """
        Translates festival names, reasons, and signals to target language using TranslationService.
        """
        try:
            from ai.translation.translation_service import get_translation_service
            translator = get_translation_service(self.db)

            translated_list = []
            for item in recommendations:
                trans_name = translator.translate_text(item.festival_name, target_language=target_language)
                trans_reason = translator.translate_text(item.match_reason, target_language=target_language)
                trans_signals = [translator.translate_text(sig, target_language=target_language) for sig in item.explanation_signals]
                trans_desc = translator.translate_text(item.description[:200], target_language=target_language)

                item_dict = item.model_dump()
                item_dict["festival_name"] = trans_name
                item_dict["match_reason"] = trans_reason
                item_dict["explanation_signals"] = trans_signals
                item_dict["description"] = trans_desc
                translated_list.append(RecommendationItem(**item_dict))

            return translated_list
        except Exception as e:
            logger.error(f"Error translating recommendations to '{target_language}': {e}. Returning original language.")
            return recommendations
