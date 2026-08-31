import sys
import logging
import numpy as np
from sqlalchemy.orm import Session
from database.connection import SessionLocal, Base, engine
from database.models import Festival
from ai.recommendation.embedding_service import get_embedding_service
from ai.recommendation.faiss_service import FAISSService

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("index_manager")


class IndexManager:
    def __init__(self, db: Session = None):
        self.db = db
        self.embedding_service = get_embedding_service()
        self.faiss_service = FAISSService(vector_dimension=self.embedding_service.vector_dimension)

    def rebuild_index(self) -> int:
        """
        Fetches all published & verified festivals from DB, constructs dynamic embedding texts,
        encodes vectors, and rebuilds the FAISS index.
        """
        close_db = False
        if self.db is None:
            self.db = SessionLocal()
            close_db = True

        try:
            festivals = self.db.query(Festival).filter(
                Festival.is_published == True,
                Festival.verification_status == "verified"
            ).all()

            logger.info(f"Found {len(festivals)} published festivals in database for FAISS index rebuild.")

            if not festivals:
                self.faiss_service.build_index([], np.empty((0, self.embedding_service.vector_dimension), dtype=np.float32))
                return 0

            festival_ids = [f.id for f in festivals]
            texts = [f.to_embedding_text() for f in festivals]

            logger.info("Generating embeddings for festival documents...")
            vectors = self.embedding_service.encode_documents(texts)

            logger.info("Building FAISS index...")
            self.faiss_service.build_index(festival_ids, vectors)
            logger.info(f"Index rebuild complete. Total indexed vectors: {self.faiss_service.get_total_vectors()}")
            return len(festival_ids)

        finally:
            if close_db:
                self.db.close()

    def index_festival(self, festival_id: str) -> bool:
        """
        Indexes or updates a single festival vector incrementally in FAISS.
        If festival is unpublished or deleted, removes it from FAISS.
        """
        close_db = False
        if self.db is None:
            self.db = SessionLocal()
            close_db = True

        try:
            festival = self.db.query(Festival).filter(Festival.id == festival_id).first()
            if not festival or not festival.is_published or festival.verification_status != "verified":
                logger.info(f"Festival '{festival_id}' is deleted/unpublished. Removing from FAISS index if present.")
                self.faiss_service.remove_vector(festival_id)
                return False

            text = festival.to_embedding_text()
            vector = self.embedding_service.encode_text(text)
            self.faiss_service.add_vector(festival_id, vector)
            return True

        finally:
            if close_db:
                self.db.close()

    def remove_festival(self, festival_id: str):
        """
        Removes a festival vector from FAISS.
        """
        self.faiss_service.remove_vector(festival_id)

    def get_status(self) -> dict:
        return {
            "total_vectors": self.faiss_service.get_total_vectors(),
            "faiss_index_path": str(self.faiss_service.index_path),
            "vector_dimension": self.faiss_service.vector_dimension
        }


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "rebuild"
    manager = IndexManager()

    if command in ("rebuild", "build"):
        count = manager.rebuild_index()
        print(f"Successfully built FAISS index with {count} festivals.")
    elif command == "status":
        status = manager.get_status()
        print(f"FAISS Index Status: {status}")
    else:
        print(f"Unknown command '{command}'. Usage: python -m ai.recommendation.index_manager [rebuild|status]")


if __name__ == "__main__":
    main()
