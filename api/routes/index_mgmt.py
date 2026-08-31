import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from ai.models.schemas import IndexStatusResponse
from ai.recommendation.index_manager import IndexManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai/index", tags=["FAISS Vector Index Management"])


@router.get(
    "/status",
    response_model=IndexStatusResponse,
    summary="Get FAISS Vector Index Status"
)
def get_faiss_index_status(db: Session = Depends(get_db)):
    try:
        manager = IndexManager(db)
        stat = manager.get_status()
        return IndexStatusResponse(
            success=True,
            total_indexed_vectors=stat["total_vectors"],
            faiss_index_path=stat["faiss_index_path"]
        )
    except Exception as e:
        logger.error(f"Error fetching index status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/rebuild",
    response_model=IndexStatusResponse,
    summary="Rebuild FAISS Vector Index",
    description="Fetches all published & verified festivals from database, generates embeddings, and rebuilds FAISS index."
)
def rebuild_faiss_index(db: Session = Depends(get_db)):
    try:
        manager = IndexManager(db)
        count = manager.rebuild_index()
        stat = manager.get_status()
        return IndexStatusResponse(
            success=True,
            total_indexed_vectors=count,
            faiss_index_path=stat["faiss_index_path"],
            message=f"FAISS index rebuilt successfully with {count} festival vectors."
        )
    except Exception as e:
        logger.error(f"Error rebuilding FAISS index: {e}")
        raise HTTPException(status_code=500, detail=str(e))
