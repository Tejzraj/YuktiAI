import logging
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from config import settings
from database.models import Festival, FestivalTranslation
from ai.translation.language_detector import detect_language
from ai.translation.cache import TranslationCacheManager
from ai.translation.providers.base import TranslationProvider
from ai.translation.providers.google_provider import GoogleTranslationProvider
from ai.translation.providers.libretranslate_provider import LibreTranslateProvider
from ai.translation.providers.mock_provider import MockTranslationProvider
from ai.models.schemas import FestivalTranslationResponse

logger = logging.getLogger(__name__)


class TranslationService:
    def __init__(self, db: Session, provider: Optional[TranslationProvider] = None):
        self.db = db
        self.cache_manager = TranslationCacheManager(db)
        self.primary_provider = provider or self._get_configured_provider()
        self.fallback_provider = MockTranslationProvider()

    def _get_configured_provider(self) -> TranslationProvider:
        prov_name = settings.TRANSLATION_PROVIDER.lower().strip()
        if prov_name == "google":
            return GoogleTranslationProvider()
        elif prov_name == "libretranslate":
            return LibreTranslateProvider()
        else:
            return MockTranslationProvider()

    def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None
    ) -> str:
        """
        Translates single text string from source to target language with caching and fallbacks.
        Never crashes; returns original text if all providers fail.
        """
        if not text or not text.strip():
            return text

        target_lang = target_language.lower().strip()
        if target_lang not in ("en", "kn", "hi"):
            target_lang = "en"

        src_lang = source_language.lower().strip() if source_language else detect_language(text)

        if src_lang == target_lang:
            return text

        # 1. Check persistent DB cache
        cached_text = self.cache_manager.get(src_lang, target_lang, text)
        if cached_text:
            return cached_text

        # 2. Call primary translation provider
        try:
            translated = self.primary_provider.translate(text, src_lang, target_lang)
            if translated and translated.strip():
                self.cache_manager.set(src_lang, target_lang, text, translated)
                return translated
        except Exception as e:
            logger.warning(f"Primary translation provider '{settings.TRANSLATION_PROVIDER}' failed: {e}")

        # 3. Call fallback mock provider
        try:
            translated = self.fallback_provider.translate(text, src_lang, target_lang)
            if translated and translated.strip():
                self.cache_manager.set(src_lang, target_lang, text, translated)
                return translated
        except Exception as e:
            logger.warning(f"Fallback translation provider failed: {e}")

        # 4. Ultimate fallback: Return original text
        return text

    def translate_batch(
        self,
        texts: List[str],
        target_language: str,
        source_language: Optional[str] = None
    ) -> List[str]:
        """
        Translates a batch list of strings.
        """
        return [self.translate_text(t, target_language, source_language) for t in texts]

    def translate_festival_fields(
        self,
        festival_id: str,
        target_language: str
    ) -> FestivalTranslationResponse:
        """
        Translates structured festival content into target language.
        First checks if structured DB translations exist in `festival_translations` table.
        Otherwise translates fields dynamically and caches results without altering original DB fields.
        """
        festival = self.db.query(Festival).filter(Festival.id == festival_id).first()
        if not festival:
            raise ValueError(f"Festival with ID '{festival_id}' not found.")

        target_lang = target_language.lower().strip()
        if target_lang == "en":
            return FestivalTranslationResponse(
                success=True,
                festival_id=festival.id,
                language="en",
                name=festival.name,
                category=festival.category,
                description=festival.description,
                history=festival.history,
                cultural_significance=festival.cultural_significance,
                activities=festival.get_activities_list(),
                food=festival.get_food_list(),
                tourist_info=festival.tourist_info
            )

        # Check DB table for existing stored translations
        db_translations = self.db.query(FestivalTranslation).filter(
            FestivalTranslation.festival_id == festival_id,
            FestivalTranslation.language == target_lang
        ).all()

        trans_map = {t.field_name: t.translated_text for t in db_translations}

        def get_or_trans(field_name: str, original_val: Optional[str]) -> str:
            if not original_val:
                return ""
            if field_name in trans_map:
                return trans_map[field_name]
            # Translate dynamically and save to FestivalTranslation DB table
            translated = self.translate_text(original_val, target_language=target_lang, source_language="en")
            try:
                record = FestivalTranslation(
                    festival_id=festival_id,
                    language=target_lang,
                    field_name=field_name,
                    translated_text=translated,
                    content_version=festival.content_version
                )
                self.db.add(record)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                logger.warning(f"Error saving FestivalTranslation record for field '{field_name}': {e}")
            return translated

        trans_name = get_or_trans("name", festival.name)
        trans_category = get_or_trans("category", festival.category)
        trans_desc = get_or_trans("description", festival.description)
        trans_history = get_or_trans("history", festival.history)
        trans_cultural = get_or_trans("cultural_significance", festival.cultural_significance)
        trans_tourist = get_or_trans("tourist_info", festival.tourist_info)

        activities = festival.get_activities_list()
        translated_activities = [self.translate_text(act, target_language=target_lang, source_language="en") for act in activities]

        food = festival.get_food_list()
        translated_food = [self.translate_text(f, target_language=target_lang, source_language="en") for f in food]

        return FestivalTranslationResponse(
            success=True,
            festival_id=festival.id,
            language=target_lang,
            name=trans_name,
            category=trans_category,
            description=trans_desc,
            history=trans_history,
            cultural_significance=trans_cultural,
            activities=translated_activities,
            food=translated_food,
            tourist_info=trans_tourist
        )


def get_translation_service(db: Session) -> TranslationService:
    return TranslationService(db)
