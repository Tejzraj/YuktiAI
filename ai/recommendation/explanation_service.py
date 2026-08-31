import logging
from typing import List, Dict, Any, Optional
from database.models import Festival
from ai.models.schemas import TouristPreferenceInput

logger = logging.getLogger(__name__)


class ExplanationService:
    @staticmethod
    def generate_explanation(
        festival: Festival,
        scores: Dict[str, Any],
        preferences: TouristPreferenceInput
    ) -> Dict[str, Any]:
        """
        Generates dynamic, evidence-backed matching reasons and explanation bullet signals.
        """
        signals = []
        matched_interests = []

        # 1. Check interest / category matching
        if preferences.interests:
            fest_tags = [t.lower() for t in festival.get_tags_list()]
            fest_cats = [c.lower().strip() for c in festival.category.split(",")]
            all_fest_terms = fest_tags + fest_cats

            for interest in preferences.interests:
                int_lower = interest.lower().strip()
                for term in all_fest_terms:
                    if int_lower in term or term in int_lower:
                        matched_interests.append(interest.title())
                        break

        if matched_interests:
            unique_matched = list(dict.fromkeys(matched_interests))
            interests_str = ", ".join(unique_matched)
            signals.append(f"You selected {interests_str}")

        # 2. Check date overlap signal
        date_score = scores.get("date_score", 0.0)
        if date_score >= 0.95 and festival.start_date:
            signals.append("The festival occurs during your travel period")
        elif date_score >= 0.6 and festival.start_date:
            signals.append(f"The festival takes place near your selected travel dates ({festival.start_date})")

        # 3. Check location / distance signal
        distance_km = scores.get("distance_km")
        location_score = scores.get("location_score", 0.0)

        if distance_km is not None:
            if distance_km <= 25.0:
                signals.append(f"The festival is in your immediate location (~{distance_km} km away)")
            elif distance_km <= 200.0:
                signals.append(f"The festival is easily accessible from your location (~{int(distance_km)} km away)")
        elif location_score >= 0.8:
            signals.append(f"Located in {festival.district}, {festival.state}")

        # 4. Check semantic relevance signal
        semantic_score = scores.get("semantic_score", 0.0)
        if semantic_score >= 0.7:
            signals.append(f"High cultural resonance with your preferences ({festival.category})")

        # Build natural narrative match reason
        if matched_interests:
            joined = " and ".join(list(dict.fromkeys(matched_interests))[:3])
            reason = f"Strong match for your interest in {joined}."
        elif semantic_score >= 0.6:
            reason = f"Excellent cultural experience matching your travel style and preferences in {festival.district}."
        else:
            reason = f"Recommended festival highlighting the traditional culture of {festival.district}."

        return {
            "match_reason": reason,
            "explanation_signals": signals
        }
