import re
import logging

logger = logging.getLogger(__name__)

# Unicode ranges for detection
KANNADA_PATTERN = re.compile(r'[\u0C80-\u0CFF]')
HINDI_PATTERN = re.compile(r'[\u0900-\u097F]')


def detect_language(text: str) -> str:
    """
    Detects language code ('en', 'kn', 'hi') from text input.
    Uses fast Unicode character matching followed by langdetect library fallback.
    """
    if not text or not text.strip():
        return "en"

    kn_chars = len(KANNADA_PATTERN.findall(text))
    hi_chars = len(HINDI_PATTERN.findall(text))

    if kn_chars > 0 and kn_chars >= hi_chars:
        return "kn"
    if hi_chars > 0 and hi_chars > kn_chars:
        return "hi"

    try:
        from langdetect import detect
        detected = detect(text)
        if detected in ("kn", "hi", "en"):
            return detected
    except Exception as e:
        logger.debug(f"langdetect fallback error: {e}")

    return "en"
