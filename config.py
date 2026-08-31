import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Sanskriti AI - Karnataka Cultural Tourism Subsystem"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    # AI / Embedding Settings
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    FAISS_INDEX_PATH: str = "data/faiss_index.bin"
    FAISS_MAPPING_PATH: str = "data/faiss_id_mapping.json"
    FAISS_TOP_K: int = 20
    RECOMMENDATION_TOP_N: int = 10

    # Hybrid Ranking Weights
    SEMANTIC_WEIGHT: float = 0.50
    LOCATION_WEIGHT: float = 0.20
    DATE_WEIGHT: float = 0.20
    CATEGORY_WEIGHT: float = 0.10

    # Multilingual & Translation Settings
    DEFAULT_LANGUAGE: str = "en"
    TRANSLATION_PROVIDER: str = "google"  # google | libretranslate | mock
    TRANSLATION_API_KEY: str = ""
    TRANSLATION_API_URL: str = ""
    TRANSLATION_CACHE_TTL_DAYS: int = 30

    # Database Settings
    DATABASE_URL: str = "sqlite:///./sanskriti_ai.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def get_faiss_index_abs_path(self) -> Path:
        path = Path(self.FAISS_INDEX_PATH)
        if not path.is_absolute():
            path = Path(__file__).parent / path
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def get_faiss_mapping_abs_path(self) -> Path:
        path = Path(self.FAISS_MAPPING_PATH)
        if not path.is_absolute():
            path = Path(__file__).parent / path
        path.parent.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
