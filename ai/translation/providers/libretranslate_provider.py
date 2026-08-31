import logging
import httpx
from config import settings
from ai.translation.providers.base import TranslationProvider

logger = logging.getLogger(__name__)


class LibreTranslateProvider(TranslationProvider):
    def __init__(self, api_url: str = None, api_key: str = None):
        self.api_url = api_url or settings.TRANSLATION_API_URL or "https://libretranslate.com/translate"
        self.api_key = api_key or settings.TRANSLATION_API_KEY

    def translate(self, text: str, source_language: str, target_language: str) -> str:
        if not text or not text.strip():
            return text

        payload = {
            "q": text,
            "source": source_language or "auto",
            "target": target_language,
            "format": "text"
        }
        if self.api_key:
            payload["api_key"] = self.api_key

        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.post(self.api_url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                return data["translatedText"]
        except Exception as e:
            logger.warning(f"LibreTranslate provider error: {e}")
            raise Exception(f"LibreTranslate provider error: {e}")
