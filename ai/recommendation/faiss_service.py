import json
import logging
import os
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import faiss
import numpy as np
from config import settings

logger = logging.getLogger(__name__)


class FAISSService:
    def __init__(self, vector_dimension: int = 384):
        self.vector_dimension = vector_dimension
        self.index_path = settings.get_faiss_index_abs_path()
        self.mapping_path = settings.get_faiss_mapping_abs_path()
        
        # FAISS IndexFlatIP (Inner Product = Cosine Similarity for normalized vectors)
        self.index: Optional[faiss.IndexFlatIP] = None
        self.id_mapping: List[str] = []  # Index position -> festival_id string
        
        self.load_or_create_index()

    def load_or_create_index(self):
        """
        Loads index and mapping from disk if available; otherwise initializes an empty index.
        """
        if self.index_path.exists() and self.mapping_path.exists():
            try:
                self.index = faiss.read_index(str(self.index_path))
                with open(self.mapping_path, "r", encoding="utf-8") as f:
                    self.id_mapping = json.load(f)
                
                # Check vector dimension compatibility
                if self.index.d != self.vector_dimension:
                    logger.warning(
                        f"FAISS index dimension ({self.index.d}) mismatch with model dimension ({self.vector_dimension}). Resetting index."
                    )
                    self._reset_index()
                else:
                    logger.info(f"Loaded existing FAISS index from disk with {self.index.ntotal} vectors.")
                return
            except Exception as e:
                logger.error(f"Failed to load FAISS index from disk: {e}. Re-initializing empty index.")

        self._reset_index()

    def _reset_index(self):
        self.index = faiss.IndexFlatIP(self.vector_dimension)
        self.id_mapping = []

    def save_index(self):
        """
        Persists the FAISS index and festival ID mapping to disk.
        """
        try:
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self.index, str(self.index_path))
            with open(self.mapping_path, "w", encoding="utf-8") as f:
                json.dump(self.id_mapping, f, indent=2)
            logger.info(f"Saved FAISS index ({self.index.ntotal} vectors) to {self.index_path}")
        except Exception as e:
            logger.error(f"Error saving FAISS index to disk: {e}")
            raise e

    def build_index(self, festival_ids: List[str], vectors: np.ndarray):
        """
        Rebuilds the index completely with the given festival IDs and 2D vector matrix [N, dimension].
        """
        self._reset_index()

        if len(festival_ids) == 0 or vectors.shape[0] == 0:
            logger.info("Empty vectors dataset provided for FAISS index build.")
            self.save_index()
            return

        if len(festival_ids) != vectors.shape[0]:
            raise ValueError(f"Length mismatch: {len(festival_ids)} IDs vs {vectors.shape[0]} vectors.")

        # Ensure vector type is float32
        vectors = vectors.astype(np.float32)
        self.index.add(vectors)
        self.id_mapping = list(festival_ids)
        self.save_index()
        logger.info(f"Successfully built FAISS index with {self.index.ntotal} festival vectors.")

    def add_vector(self, festival_id: str, vector: np.ndarray):
        """
        Incrementally adds or updates a festival vector in the FAISS index.
        """
        if vector.ndim == 1:
            vector = np.expand_dims(vector, axis=0)

        vector = vector.astype(np.float32)

        # If festival already exists, remove it first
        if festival_id in self.id_mapping:
            self.remove_vector(festival_id)

        self.index.add(vector)
        self.id_mapping.append(festival_id)
        self.save_index()
        logger.info(f"Incrementally added vector for festival ID '{festival_id}' to FAISS index.")

    def remove_vector(self, festival_id: str):
        """
        Removes a festival ID from the index by filtering and rebuilding remaining vectors.
        """
        if festival_id not in self.id_mapping:
            return

        idx = self.id_mapping.index(festival_id)
        # Re-construct remaining vectors from index
        n = self.index.ntotal
        remaining_ids = []
        remaining_vectors = []

        for i in range(n):
            if i != idx:
                vec = self.index.reconstruct(i)
                remaining_ids.append(self.id_mapping[i])
                remaining_vectors.append(vec)

        if remaining_vectors:
            vec_matrix = np.array(remaining_vectors, dtype=np.float32)
        else:
            vec_matrix = np.empty((0, self.vector_dimension), dtype=np.float32)

        self.build_index(remaining_ids, vec_matrix)
        logger.info(f"Removed festival ID '{festival_id}' from FAISS index.")

    def search(self, query_vector: np.ndarray, top_k: int = 20) -> List[Tuple[str, float]]:
        """
        Searches the FAISS index for the top-k most similar festival vectors.
        Returns a list of tuples: [(festival_id, similarity_score)].
        Cosine similarity range: -1.0 to 1.0 (typically 0.0 to 1.0 for normalized text vectors).
        """
        if self.index.ntotal == 0 or len(self.id_mapping) == 0:
            logger.info("FAISS index is empty. Returning 0 candidate matches.")
            return []

        if query_vector.ndim == 1:
            query_vector = np.expand_dims(query_vector, axis=0)

        query_vector = query_vector.astype(np.float32)
        actual_k = min(top_k, self.index.ntotal)

        # Search FAISS index
        scores, indices = self.index.search(query_vector, actual_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.id_mapping):
                fest_id = self.id_mapping[idx]
                sim_score = float(scores[0][i])
                # Clip similarity score to [0.0, 1.0] for standard semantic range
                sim_score = max(0.0, min(1.0, sim_score))
                results.append((fest_id, sim_score))

        return results

    def get_total_vectors(self) -> int:
        return self.index.ntotal if self.index else 0
