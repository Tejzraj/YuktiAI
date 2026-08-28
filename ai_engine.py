"""
YuktiAI - AI Recommendation & Multilingual Engine
Member 2: Nandish
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Union

# Try importing sentence_transformers & torch safely
HAS_SENTENCE_TRANSFORMERS = False
try:
    import torch
    from sentence_transformers import SentenceTransformer, util
    HAS_SENTENCE_TRANSFORMERS = True
except Exception:
    HAS_SENTENCE_TRANSFORMERS = False

# Try importing scikit-learn TfidfVectorizer & cosine_similarity
HAS_SKLEARN = False
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except Exception:
    HAS_SKLEARN = False

# Try importing deep_translator
HAS_DEEP_TRANSLATOR = False
try:
    from deep_translator import GoogleTranslator
    HAS_DEEP_TRANSLATOR = True
except Exception:
    HAS_DEEP_TRANSLATOR = False

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "yuktiai"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password123"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}


def load_festivals_dataset() -> List[Dict[str, Any]]:
    """Load festivals dataset from PostgreSQL or JSON fallback file."""
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(**DB_CONFIG, connect_timeout=1, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.id, f.name, f.district, f.short_description as description, 
                   f.cultural_significance, f.major_attractions, f.local_food, f.activities as tags,
                   c.name as category
            FROM festivals f
            LEFT JOIN festival_categories c ON f.category_id = c.id
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows:
            data = []
            for r in rows:
                item = dict(r)
                item["attractions"] = item.get("major_attractions") or []
                item["tags"] = item.get("tags") or []
                item["local_food"] = item.get("local_food") or []
                data.append(item)
            return data
    except Exception:
        pass

    candidates = [
        Path(__file__).parent / "yuktiai" / "festivals_karnataka.json",
        Path(__file__).parent / "festivals_karnataka.json",
        Path.cwd() / "yuktiai" / "festivals_karnataka.json",
        Path.cwd() / "festivals_karnataka.json",
    ]
    for p in candidates:
        if p.is_file():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

    return [
        {
            "id": "mysuru-dasara",
            "name": "Mysuru Dasara",
            "district": "Mysuru",
            "category": "State Festival & Royal Heritage",
            "description": "Royal state festival featuring royal heritage, food, illuminations, and elephant procession.",
            "attractions": ["Jamboo Savari", "Palace Illumination"],
            "local_food": ["Mysore Pak", "Masala Dosa"],
            "tags": ["royal", "heritage", "food", "folk", "culture"]
        },
        {
            "id": "kambala-race",
            "name": "Kambala Buffalo Race",
            "district": "Dakshina Kannada",
            "category": "Folk & Sports",
            "description": "Traditional coastal slush track buffalo race showcasing coastal folk tradition.",
            "attractions": ["Buffalo Race", "Coastal Folk Music"],
            "local_food": ["Kori Rotti", "Neer Dosa"],
            "tags": ["folk", "sports", "coastal", "culture", "tradition"]
        },
        {
            "id": "hampi-utsav",
            "name": "Hampi Utsav",
            "district": "Vijayanagara",
            "category": "Heritage & Art",
            "description": "Grand cultural festival celebrating Vijayanagara architecture, dance, music and drama.",
            "attractions": ["Light Show", "Classical Dance"],
            "local_food": ["Jowar Rotti", "Shenga Chutney"],
            "tags": ["heritage", "art", "music", "dance", "culture"]
        }
    ]


class AIEngine:
    def __init__(self):
        self.festivals = load_festivals_dataset()
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.festival_texts = []
        self._init_tfidf()

    def _build_festival_text(self, fest: Dict[str, Any]) -> str:
        name = fest.get("name", "")
        cat = fest.get("category", "")
        desc = fest.get("description") or fest.get("short_description") or ""
        significance = fest.get("cultural_significance", "")
        attraction_list = fest.get("attractions") or fest.get("major_attractions") or []
        attractions = " ".join(attraction_list) if isinstance(attraction_list, list) else str(attraction_list)
        food_list = fest.get("local_food") or []
        food = " ".join(food_list) if isinstance(food_list, list) else str(food_list)
        tag_list = fest.get("tags") or fest.get("activities") or []
        tags = " ".join(tag_list) if isinstance(tag_list, list) else str(tag_list)
        return f"{name} {cat} {desc} {significance} {attractions} {food} {tags}".lower()

    def _init_tfidf(self):
        """Initialize fast TF-IDF vectorizer immediately."""
        self.festival_texts = [self._build_festival_text(f) for f in self.festivals]
        if HAS_SKLEARN and self.festival_texts:
            try:
                self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
                self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.festival_texts)
            except Exception as e:
                print(f"⚠️ Could not initialize TF-IDF vectorizer: {e}")

    def recommend(self, interests: List[str]) -> List[Dict[str, Any]]:
        """Calculate recommendations based on TF-IDF Cosine Similarity or Keyword Vector Overlap."""
        if not interests or not self.festivals:
            return []

        user_query = " ".join(interests).lower()

        # Strategy A: Fast Scikit-Learn TF-IDF Cosine Similarity
        if self.tfidf_vectorizer is not None and self.tfidf_matrix is not None:
            try:
                query_vec = self.tfidf_vectorizer.transform([user_query])
                sim_scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]
                results = []
                for i, fest in enumerate(self.festivals):
                    raw_score = float(sim_scores[i])
                    # Score formatting (0-100)
                    score = round(max(0.0, min(99.0, raw_score * 100 + 20.0 if raw_score > 0 else 10.0)), 2)
                    fest_id = fest.get("id") or fest.get("festival_id")
                    results.append({
                        "festival_id": fest_id,
                        "name": fest.get("name"),
                        "district": fest.get("district"),
                        "category": fest.get("category"),
                        "score": score
                    })
                results.sort(key=lambda x: x["score"], reverse=True)
                return results
            except Exception as e:
                print(f"⚠️ TF-IDF recommendation error: {e}")

        # Strategy B: Keyword Overlap Vector Matcher
        results = []
        interest_tokens = set(user_query.lower().split())
        for fest in self.festivals:
            text = self._build_festival_text(fest)
            fest_tokens = set(text.split())
            if not fest_tokens or not interest_tokens:
                score = 0.0
            else:
                intersection = interest_tokens.intersection(fest_tokens)
                score = round((len(intersection) / max(1, len(interest_tokens))) * 80.0 + 10.0, 2)
            fest_id = fest.get("id") or fest.get("festival_id")
            results.append({
                "festival_id": fest_id,
                "name": fest.get("name"),
                "district": fest.get("district"),
                "category": fest.get("category"),
                "score": min(99.0, score)
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def translate(self, text: str, target_lang: str) -> Dict[str, Any]:
        """Translate text to target_lang ('kn', 'hi', 'en')."""
        target_lang = target_lang.lower().strip()
        if target_lang in ["kannada", "kan"]:
            target_lang = "kn"
        elif target_lang in ["hindi", "hin"]:
            target_lang = "hi"
        elif target_lang in ["english", "eng"]:
            target_lang = "en"

        if HAS_DEEP_TRANSLATOR and target_lang in ["kn", "hi", "en"]:
            try:
                translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
                return {
                    "original_text": text,
                    "target_lang": target_lang,
                    "translated_text": translated
                }
            except Exception as e:
                print(f"⚠️ Translation fallback triggered: {e}")

        # Dictionary Fallback for Offline / Mock testing
        kannada_dict = {
            "welcome": "ಸ್ವಾಗತ",
            "festival": "ಹಬ್ಬ",
            "culture": "ಸಂಸ್ಕೃತಿ",
            "food": "ಆಹಾರ",
            "heritage": "ಪಾರಂಪರಿಕ"
        }
        hindi_dict = {
            "welcome": "स्वागत है",
            "festival": "त्यौहार",
            "culture": "संस्कृति",
            "food": "भोजन",
            "heritage": "विरासत"
        }

        words = text.lower().split()
        translated_words = []
        for w in words:
            clean_w = w.strip(".,!?")
            if target_lang == "kn" and clean_w in kannada_dict:
                translated_words.append(kannada_dict[clean_w])
            elif target_lang == "hi" and clean_w in hindi_dict:
                translated_words.append(hindi_dict[clean_w])
            else:
                translated_words.append(w)
        
        translated_text = " ".join(translated_words)
        if target_lang == "kn" and translated_text == text:
            translated_text = f"[ಕನ್ನಡ] {text}"
        elif target_lang == "hi" and translated_text == text:
            translated_text = f"[हिंदी] {text}"

        return {
            "original_text": text,
            "target_lang": target_lang,
            "translated_text": translated_text
        }


# Global engine instance
ai_engine = AIEngine()
