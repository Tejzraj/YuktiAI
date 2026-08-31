import pytest
from database.connection import Base, engine, SessionLocal
from ai.translation.translation_service import TranslationService
from ai.translation.providers.mock_provider import MockTranslationProvider
from ai.translation.language_detector import detect_language


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


def test_language_detector():
    assert detect_language("ನನಗೆ ಜನಪದ ಹಬ್ಬಗಳು ಇಷ್ಟ") == "kn"
    assert detect_language("मुझे मैसूरु दशहरा पसंद है") == "hi"
    assert detect_language("I love folk festivals and local food") == "en"


def test_mock_translation_provider():
    provider = MockTranslationProvider()
    kn_res = provider.translate("Mysuru Dasara (Nada Habba)", "en", "kn")
    assert kn_res == "ಮೈಸೂರು ದಸರಾ (ನಾಡ ಹಬ್ಬ)"

    hi_res = provider.translate("Heritage", "en", "hi")
    assert hi_res == "विरासत"


def test_translation_service_caching(db_session):
    # Pass MockTranslationProvider so test doesn't depend on external network
    service = TranslationService(db_session, provider=MockTranslationProvider())

    # First call: Should compute & cache
    trans1 = service.translate_text("Traditional cultural festival", target_language="kn", source_language="en")
    assert isinstance(trans1, str) and len(trans1) > 0

    # Check cache table
    cached = service.cache_manager.get("en", "kn", "Traditional cultural festival")
    assert cached == trans1

    # Second call: Should return cached value instantly
    trans2 = service.translate_text("Traditional cultural festival", target_language="kn", source_language="en")
    assert trans2 == trans1
