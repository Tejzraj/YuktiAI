import time
import logging
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
from database.connection import engine, Base
from database.seed import seed_database
from ai.recommendation.embedding_service import get_embedding_service
from ai.recommendation.index_manager import IndexManager
from api.routes import recommendation, translation, index_mgmt, festivals

# Professional logging configuration
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("sanskriti_ai")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application Lifespan Lifecycle Manager.
    Pre-loads Sentence Transformer model into RAM and verifies FAISS vector index at startup.
    """
    logger.info("================================================================")
    logger.info(" Starting Sanskriti AI — Karnataka Cultural Tourism Subsystem ")
    logger.info("================================================================")
    
    # 1. Database Initialization
    Base.metadata.create_all(bind=engine)
    try:
        seed_database()
    except Exception as e:
        logger.warning(f"Database seed check notice: {e}")

    # 2. Embedding Model Preloading
    logger.info("Pre-loading Sentence Transformer embedding model...")
    embed_svc = get_embedding_service()
    logger.info(f"Loaded embedding model: '{embed_svc.model_name}' (Vector Dim: {embed_svc.vector_dimension})")

    # 3. FAISS Vector Store Lifecycle
    logger.info("Initializing FAISS Vector Search Index...")
    idx_mgr = IndexManager()
    total_vectors = idx_mgr.faiss_service.get_total_vectors()
    if total_vectors == 0:
        logger.info("FAISS index empty. Building index from database festival documents...")
        idx_mgr.rebuild_index()
    else:
        logger.info(f"FAISS index operational with {total_vectors} festival vectors.")

    logger.info("Sanskriti AI Subsystem is online and accepting API requests.")
    logger.info("================================================================")

    yield

    logger.info("Shutting down Sanskriti AI Subsystem...")


API_DESCRIPTION = r"""
### Sanskriti AI — Karnataka Cultural Tourism Subsystem (Member 2 Module)

Welcome to the official REST API documentation for the **Sanskriti AI Recommendation & Multilingual Subsystem**.

#### Key System Capabilities:
- **Semantic Recommendation Engine**: Powered by **Sentence Transformers** (`paraphrase-multilingual-MiniLM-L12-v2`) and **FAISS IndexFlatIP** vector search.
- **Hybrid Ranking Engine**: Blends 4 weighted signals into normalized match scores ($0-100\%$):
  - **Semantic Score (50%)**: Vector similarity between query/interests and festival documents.
  - **Location Score (20%)**: Haversine great-circle distance math.
  - **Date Score (20%)**: Temporal overlap between tourist dates and festival dates.
  - **Category Score (10%)**: Jaccard interest tag similarity.
- **Dynamic Evidence-Backed Match Explanations**: Generates real match explanations ("Why this festival matches you").
- **Multilingual Intelligence**: Supports **English (`en`)**, **Kannada (`kn` - ಕನ್ನಡ)**, and **Hindi (`hi` - हिंदी)** with persistent SHA-256 translation caching and 4-tier failure fallback.

#### System Architecture:
```text
Tourist Request -> FastAPI Router -> Recommendation Service -> Embedding Model + FAISS Index -> Hybrid Ranker -> Localized Output
```
"""

app = FastAPI(
    title="Sanskriti AI — Cultural Tourism Platform Subsystem",
    version="1.0.0",
    description=API_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Process Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time-MS"] = str(round(process_time * 1000, 2))
    return response


# Professional Uniform Error Handlers
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "path": request.url.path,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
    )


@app.exception_handler(Exception)
async def custom_global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled system error on path '{request.url.path}': {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "An internal server error occurred while processing your request.",
                "path": request.url.path,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
    )


# Register API Routers
app.include_router(recommendation.router)
app.include_router(translation.router)
app.include_router(index_mgmt.router)
app.include_router(festivals.router)


@app.get("/", summary="System Health & Status Endpoint", tags=["System Diagnostics"])
def health_check():
    embed_svc = get_embedding_service()
    idx_mgr = IndexManager()
    return {
        "success": True,
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "diagnostics": {
            "embedding_model": embed_svc.model_name,
            "vector_dimension": embed_svc.vector_dimension,
            "faiss_total_vectors": idx_mgr.faiss_service.get_total_vectors(),
            "default_language": settings.DEFAULT_LANGUAGE,
            "translation_provider": settings.TRANSLATION_PROVIDER
        }
    }
