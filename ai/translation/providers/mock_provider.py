import logging
from ai.translation.providers.base import TranslationProvider

logger = logging.getLogger(__name__)

# Mock translation dictionary for offline mode & deterministic unit testing
MOCK_TRANSLATIONS = {
    "kn": {
        "Mysuru Dasara (Nada Habba)": "ಮೈಸೂರು ದಸರಾ (ನಾಡ ಹಬ್ಬ)",
        "Hampi Utsav (Vijaya Utsav)": "ಹಂಪಿ ಉತ್ಸವ (ವಿಜಯ ಉತ್ಸವ)",
        "Kudla Kambala Buffalo Race": "ಕುಡ್ಲ ಕಂಬಳ ಕೋಣಗಳ ಓಟ",
        "Bengaluru Karaga Shaktyotsava": "ಬೆಂಗಳೂರು ಕರಗ ಶಕ್ತಿಉತ್ಸವ",
        "Pattadakal Dance Festival": "ಪಟ್ಟದಕಲ್ಲು ನೃತ್ಯೋತ್ಸವ",
        "Melukote Vairamudi Brahmotsava": "ಮೇಲುಕೋಟೆ ವೈರಮುಡಿ ಬ್ರಹ್ಮೋತ್ಸವ",
        "Bengaluru Kadalekai Parishe (Groundnut Fair)": "ಬೆಂಗಳೂರು ಕಡಲೆಕಾಯಿ ಪರಿಷೆ",
        "Udupi Coastal Yakshagana Festival": "ಉಡುಪಿ ಕರಾವಳಿ ಯಕ್ಷಗಾನ ಮಹೋತ್ಸವ",
        "Traditional cultural festival": "ಪಾರಂಪರಿಕ ಸಾಂಸ್ಕೃತಿಕ ಹಬ್ಬ",
        "Heritage": "ಪಾರಂಪರಿಕ",
        "Folk": "ಜನಪದ",
        "Religious": "ಧಾರ್ಮಿಕ",
        "Food": "ಆಹಾರ ಮತ್ತು ತಿನಿಸು",
        "Location": "ಸ್ಥಳ",
        "Activities": "ಚಟುವಟಿಕೆಗಳು",
        "Cultural Significance": "ಸಾಂಸ್ಕೃತಿಕ ಮಹತ್ವ",
        "History": "ಇತಿಹಾಸ",
        "Nearby Attractions": "ಹತ್ತಿರದ ಆಕರ್ಷಣೆಗಳು",
        "Plan Trip": "ಪ್ರವಾಸ ಯೋಜನೆ",
        "Recommended For You": "ನಿಮಗಾಗಿ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ",
        "Why this festival matches you": "ಈ ಹಬ್ಬವು ನಿಮಗೆ ಏಕೆ ಸೂಕ್ತವಾಗಿದೆ",
        "Strong match for your interest in Folk Culture and Heritage.": "ಜನಪದ ಸಂಸ್ಕೃತಿ ಮತ್ತು ಪಾರಂಪರಿಕ ಆಸಕ್ತಿಗೆ ಉತ್ತಮ ಹೊಂದಾಣಿಕೆ."
    },
    "hi": {
        "Mysuru Dasara (Nada Habba)": "मैसूरु दशहरा (नाडा हब्बा)",
        "Hampi Utsav (Vijaya Utsav)": "हम्पी उत्सव (विजया उत्सव)",
        "Kudla Kambala Buffalo Race": "कुडला कंबाला भैंसा दौड़",
        "Bengaluru Karaga Shaktyotsava": "बेंगलुरु करगा शक्तिउत्सव",
        "Pattadakal Dance Festival": "पट्टादकल नृत्य महोत्सव",
        "Melukote Vairamudi Brahmotsava": "मेलुकोटे वैरामुडी ब्रह्मोत्सव",
        "Bengaluru Kadalekai Parishe (Groundnut Fair)": "बेंगलुरु कडालेकाई पारिशे (मूंगफली मेला)",
        "Udupi Coastal Yakshagana Festival": "उडुपी तटीय यक्षगान महोत्सव",
        "Traditional cultural festival": "पारंपरिक सांस्कृतिक त्योहार",
        "Heritage": "विरासत",
        "Folk": "लोक संस्कृति",
        "Religious": "धार्मिक",
        "Food": "व्यंजन एवं भोजन",
        "Location": "स्थान",
        "Activities": "गतिविधियां",
        "Cultural Significance": "सांस्कृतिक महत्व",
        "History": "इतिहास",
        "Recommended For You": "आपके लिए अनुशंसित",
        "Why this festival matches you": "यह त्योहार आपके लिए क्यों उपयुक्त है",
        "Strong match for your interest in Folk Culture and Heritage.": "लोक संस्कृति और विरासत में आपकी रुचि का मजबूत मैच।"
    }
}


class MockTranslationProvider(TranslationProvider):
    def translate(self, text: str, source_language: str, target_language: str) -> str:
        if source_language.lower() == target_language.lower():
            return text

        lang_dict = MOCK_TRANSLATIONS.get(target_language.lower(), {})
        if text in lang_dict:
            return lang_dict[text]

        # Dynamic mock prefixing if exact string not in mock dictionary
        if target_language.lower() == "kn":
            return f"[ಕನ್ನಡ] {text}"
        elif target_language.lower() == "hi":
            return f"[हिंदी] {text}"
        return text
