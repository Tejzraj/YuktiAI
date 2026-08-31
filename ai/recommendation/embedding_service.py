import logging
import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer
from config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    _instance = None

    def __new__(cls, model_name: str = None):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_name: str = None):
        if self._initialized:
            return
        self.model_name = model_name or settings.EMBEDDING_MODEL
        logger.info(f"Initializing Sentence Transformer embedding model: {self.model_name}")
        try:
            self.model = SentenceTransformer(self.model_name)
            if hasattr(self.model, "get_embedding_dimension"):
                self._vector_dim = self.model.get_embedding_dimension()
            else:
                self._vector_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"Model {self.model_name} loaded successfully with vector dimension {self._vector_dim}")
        except Exception as e:
            logger.error(f"Failed to load sentence transformer model {self.model_name}: {e}")
            raise e
        self._initialized = True

    @property
    def vector_dimension(self) -> int:
        return self._vector_dim

    def encode_text(self, text: str) -> np.ndarray:
        """
        Encodes a single text string into a normalized 1D float32 vector array.
        """
        if not text or not text.strip():
            return np.zeros((self._vector_dim,), dtype=np.float32)
        
        vector = self.model.encode(text.strip(), convert_to_numpy=True, normalize_embeddings=True)
        return vector.astype(np.float32)

    def encode_documents(self, texts: List[str]) -> np.ndarray:
        """
        Encodes a list of text strings into a normalized 2D float32 numpy array [N, dimension].
        """
        if not texts:
            return np.empty((0, self._vector_dim), dtype=np.float32)

        cleaned_texts = [t.strip() if t and t.strip() else " " for t in texts]
        embeddings = self.model.encode(cleaned_texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.astype(np.float32)


_embedding_service_instance = None


def get_embedding_service() -> EmbeddingService:
    global _embedding_service_instance
    if _embedding_service_instance is None:
        _embedding_service_instance = EmbeddingService()
    return _embedding_service_instance
