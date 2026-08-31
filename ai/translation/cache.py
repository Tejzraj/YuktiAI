import hashlib
import logging
from typing import Optional
from sqlalchemy.orm import Session
from database.models import TranslationCache

logger = logging.getLogger(__name__)


class TranslationCacheManager:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def generate_key(source_lang: str, target_lang: str, text: str) -> str:
        text_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:16]
        return f"{source_lang.lower()}_{target_lang.lower()}_{text_hash}"

    def get(self, source_lang: str, target_lang: str, text: str) -> Optional[str]:
        cache_key = self.generate_key(source_lang, target_lang, text)
        try:
            cached = self.db.query(TranslationCache).filter(TranslationCache.cache_key == cache_key).first()
            if cached:
                logger.debug(f"Translation cache HIT for key '{cache_key}'")
                return cached.translated_text
        except Exception as e:
            logger.warning(f"Error querying translation cache: {e}")
        return None

    def set(self, source_lang: str, target_lang: str, original_text: str, translated_text: str):
        if not original_text or not translated_text:
            return
        cache_key = self.generate_key(source_lang, target_lang, original_text)
        text_hash = hashlib.sha256(original_text.strip().encode("utf-8")).hexdigest()
        try:
            existing = self.db.query(TranslationCache).filter(TranslationCache.cache_key == cache_key).first()
            if not existing:
                entry = TranslationCache(
                    cache_key=cache_key,
                    source_language=source_lang,
                    target_language=target_lang,
                    original_text_hash=text_hash,
                    translated_text=translated_text
                )
                self.db.add(entry)
                self.db.commit()
                logger.debug(f"Saved translation to cache with key '{cache_key}'")
        except Exception as e:
            self.db.rollback()
            logger.warning(f"Failed to write translation cache: {e}")
