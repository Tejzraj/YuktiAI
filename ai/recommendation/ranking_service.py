import math
import logging
from datetime import datetime, date
from typing import Optional, List, Dict, Tuple
from config import settings
from database.models import Festival
from ai.models.schemas import TouristPreferenceInput, LocationInput

logger = logging.getLogger(__name__)


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the great-circle distance between two points on the Earth using Haversine formula.
    """
    R = 6371.0  # Earth's radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class RankingService:
    def __init__(
        self,
        semantic_weight: float = None,
        location_weight: float = None,
        date_weight: float = None,
        category_weight: float = None
    ):
        self.semantic_weight = semantic_weight if semantic_weight is not None else settings.SEMANTIC_WEIGHT
        self.location_weight = location_weight if location_weight is not None else settings.LOCATION_WEIGHT
        self.date_weight = date_weight if date_weight is not None else settings.DATE_WEIGHT
        self.category_weight = category_weight if category_weight is not None else settings.CATEGORY_WEIGHT

        # Normalize weights to sum to 1.0
        total_w = self.semantic_weight + self.location_weight + self.date_weight + self.category_weight
        if total_w > 0:
            self.semantic_weight /= total_w
            self.location_weight /= total_w
            self.date_weight /= total_w
            self.category_weight /= total_w

    def calculate_location_score(
        self,
        tourist_location: Optional[LocationInput],
        festival: Festival
    ) -> Tuple[float, Optional[float]]:
        """
        Calculates location relevance score (0.0 to 1.0) and distance in KM.
        """
        if not tourist_location:
            return 0.8, None  # Neutral default score when tourist specifies no location

        distance_km: Optional[float] = None

        # 1. Exact coordinate distance using Haversine formula
        if (tourist_location.latitude is not None and tourist_location.longitude is not None and
                festival.latitude is not None and festival.longitude is not None):
            distance_km = haversine_distance_km(
                tourist_location.latitude, tourist_location.longitude,
                festival.latitude, festival.longitude
            )
            # 0 km -> 1.0, 500 km or more -> 0.0 linear decay
            loc_score = max(0.0, 1.0 - (distance_km / 500.0))
            return loc_score, round(distance_km, 1)

        # 2. City / District string match fallback
        if tourist_location.city:
            city_lower = tourist_location.city.lower().strip()
            fest_loc_lower = festival.location.lower()
            fest_dist_lower = festival.district.lower()

            if city_lower in fest_loc_lower or city_lower in fest_dist_lower:
                return 1.0, 10.0  # Same city/district estimate
            elif "bengaluru" in city_lower and fest_dist_lower == "bengaluru urban":
                return 1.0, 5.0
            elif "mysore" in city_lower and "mysuru" in fest_dist_lower:
                return 1.0, 5.0

        return 0.5, None

    def calculate_date_score(
        self,
        tourist_start: Optional[str],
        tourist_end: Optional[str],
        festival: Festival
    ) -> float:
        """
        Calculates date temporal relevance score (0.0 to 1.0).
        """
        if not tourist_start or not festival.start_date:
            return 0.8  # Neutral score if dates are omitted

        try:
            t_start = datetime.strptime(tourist_start, "%Y-%m-%d").date()
            t_end = datetime.strptime(tourist_end, "%Y-%m-%d").date() if tourist_end else t_start

            f_start = datetime.strptime(festival.start_date, "%Y-%m-%d").date()
            f_end = datetime.strptime(festival.end_date, "%Y-%m-%d").date() if festival.end_date else f_start

            # Check overlap: max(start1, start2) <= min(end1, end2)
            latest_start = max(t_start, f_start)
            earliest_end = min(t_end, f_end)

            if latest_start <= earliest_end:
                return 1.0  # Direct date overlap

            # If outside travel range, decay linearly based on days gap
            if f_start > t_end:
                gap_days = (f_start - t_end).days
            else:
                gap_days = (t_start - f_end).days

            # 1 to 14 days gap decays from 0.9 down to 0.0
            date_score = max(0.0, 1.0 - (gap_days / 14.0))
            return round(date_score, 2)

        except Exception as e:
            logger.warning(f"Error parsing dates for date scoring: {e}")
            return 0.5

    def calculate_category_score(
        self,
        tourist_interests: List[str],
        festival: Festival
    ) -> float:
        """
        Calculates category / interest overlap score (0.0 to 1.0).
        """
        if not tourist_interests:
            return 0.7  # Neutral default score

        fest_tags = set([t.lower() for t in festival.get_tags_list()])
        fest_category = set([c.lower().strip() for c in festival.category.split(",")])
        fest_all_concepts = fest_tags.union(fest_category)

        tourist_concepts = set([i.lower().strip() for i in tourist_interests])

        matches = 0
        for tc in tourist_concepts:
            for fc in fest_all_concepts:
                if tc in fc or fc in tc:
                    matches += 1
                    break

        score = matches / max(len(tourist_concepts), 1.0)
        return min(1.0, score)

    def rank_festival(
        self,
        semantic_score: float,
        festival: Festival,
        preferences: TouristPreferenceInput
    ) -> Dict[str, float]:
        """
        Computes individual component scores and weighted final match score.
        """
        location_score, distance_km = self.calculate_location_score(preferences.location, festival)
        date_score = self.calculate_date_score(preferences.start_date, preferences.end_date, festival)
        category_score = self.calculate_category_score(preferences.interests, festival)

        # Weighted final score
        raw_final_score = (
            (semantic_score * self.semantic_weight) +
            (location_score * self.location_weight) +
            (date_score * self.date_weight) +
            (category_score * self.category_weight)
        )

        match_score = int(round(raw_final_score * 100))
        match_score = max(0, min(100, match_score))

        return {
            "match_score": match_score,
            "semantic_score": round(semantic_score, 3),
            "location_score": round(location_score, 3),
            "date_score": round(date_score, 3),
            "category_score": round(category_score, 3),
            "distance_km": distance_km
        }
