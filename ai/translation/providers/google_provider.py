import logging
import httpx
from config import settings
from ai.translation.providers.base import TranslationProvider

logger = logging.getLogger(__name__)


class GoogleTranslationProvider(TranslationProvider):
    def __init__(self, api_key: str = None, api_url: str = None):
        self.api_key = api_key or settings.TRANSLATION_API_KEY
        self.api_url = api_url or settings.TRANSLATION_API_URL or "https://translation.googleapis.com/language/translate/v2"

    def translate(self, text: str, source_language: str, target_language: str) -> str:
        if not text or not text.strip():
            return text
        if source_language.lower() == target_language.lower():
            return text

        # 1. Official Google Translate API if API Key is configured
        if self.api_key:
            try:
                params = {
                    "key": self.api_key,
                    "q": text,
                    "target": target_language,
                    "format": "text"
                }
                if source_language:
                    params["source"] = source_language

                with httpx.Client(timeout=5.0) as client:
                    resp = client.post(self.api_url, params=params)
                    resp.raise_for_status()
                    data = resp.json()
                    translated = data["data"]["translations"][0]["translatedText"]
                    return translated
            except Exception as e:
                logger.warning(f"Google Cloud Translation API failed: {e}. Trying public fallback endpoint.")

        # 2. Public web fallback endpoint
        try:
            free_url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": source_language or "auto",
                "tl": target_language,
                "dt": "t",
                "q": text
            }
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(free_url, params=params)
                resp.raise_for_status()
                data = resp.json()
                translated = "".join([part[0] for part in data[0] if part[0]])
                if translated:
                    return translated
        except Exception as e:
            logger.warning(f"Google public translation fallback failed: {e}")

        raise Exception("Google translation service unavailable")
