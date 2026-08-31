# Sanskriti AI — AI Recommendation Engine & Multilingual Intelligence

Production-quality AI recommendation engine and multilingual intelligence subsystem for the **Karnataka Cultural Tourism Platform (SANSKRITI_AI)**.

---

## Architecture Overview

```text
                                TOURIST PREFERENCES
                                         │
                                         ▼
                             FastAPI Web Interface
                                         │
              ┌──────────────────────────┴──────────────────────────┐
              │                                                     │
              ▼                                                     ▼
     AI Recommendation API                                 Multilingual API
              │                                                     │
              ▼                                                     ▼
   Recommendation Service                                 Translation Service
              │                                                     │
      ┌───────┼───────┐                                     ┌───────┴───────┐
      ▼       ▼       ▼                                     ▼               ▼
  Embedding FAISS  Hybrid                               Provider         Database
   Model    Index  Ranking                             Abstraction        Cache
  (ST ML)  (Vec)   Engine                              (Google/Mock)        │
      │       │       │                                     │               │
      └───┬───┴───────┘                                     └───────┬───────┘
          ▼                                                         ▼
     Festival DB                                           Localized Responses
  (Published Events)                                    (EN, KN - ಕನ್ನಡ, HI - हिंदी)
```

---

## Features

### 1. Semantic Recommendation Subsystem
- **Sentence Transformers (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`)**: Encodes rich festival metadata (Name, Category, Description, History, Cultural Significance, Activities, Food, Location, Tags, Tourist Info) into dense normalized 384-dimensional vectors.
- **FAISS Vector Store (`faiss.IndexFlatIP`)**: Provides fast cosine similarity vector search. Automatically persisted to disk (`data/faiss_index.bin` + `data/faiss_id_mapping.json`) with support for full index rebuilding and real-time incremental vector updates when festivals are published or updated.
- **Hybrid Ranking Engine**: Blends 4 distinct scoring signals:
  - **Semantic Score (50%)**: Cosine similarity between tourist query/interests and festival vector.
  - **Location Score (20%)**: Haversine great-circle distance formula between tourist coordinates/location and festival venue ($1.0 - \text{distance}/500$).
  - **Date Overlap Score (20%)**: Temporal relevance matching festival start/end dates with tourist travel dates ($1.0$ for direct overlap, decaying linearly if near).
  - **Category / Interest Score (10%)**: Jaccard similarity between tourist interest keywords and festival category/tags.
- **Match Score & Dynamic Explanations**: Converts raw component scores into user-friendly integer percentages (e.g. `92% Match`) accompanied by real evidence-backed explanation signals ("Why this festival matches you").

### 2. Multilingual Subsystem
- **Supported Languages**: English (`en`), Kannada (`kn` - ಕನ್ನಡ), Hindi (`hi` - हिंदी).
- **Provider Abstraction**: Decoupled `TranslationProvider` base class supporting `GoogleTranslationProvider`, `LibreTranslateProvider`, and `MockTranslationProvider`.
- **Database-Backed Caching**: `TranslationCacheManager` stores translated strings using SHA-256 text hashes to avoid redundant external API calls and reduce latency.
- **Failure Resilience**: Automatic fallback chain (Cache -> Primary Provider -> Fallback Provider -> Original Text) ensures zero application crashes even if external translation APIs fail.
- **Structured Content Translation**: Translates structured festival fields dynamically without overwriting original database records.

---

## Directory Structure

```text
d:\SANSKRITI_AI\
├── config.py                         # App configuration & env variables (Pydantic Settings)
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variables template
├── database/
│   ├── connection.py                 # SQLAlchemy engine & session management
│   ├── models.py                     # Database schemas (Festival, FestivalTranslation, TranslationCache)
│   └── seed.py                       # Karnataka cultural festival seed dataset
├── ai/
│   ├── models/
│   │   └── schemas.py                # Pydantic request & response schemas
│   ├── recommendation/
│   │   ├── embedding_service.py      # SentenceTransformer singleton loader & encoder
│   │   ├── faiss_service.py          # FAISS vector store, disk persistence, vector CRUD
│   │   ├── ranking_service.py        # Hybrid ranking engine (Semantic + Distance + Date + Category)
│   │   ├── explanation_service.py    # Match signal explanation generator
│   │   ├── recommendation_service.py # Core orchestrator
│   │   └── index_manager.py          # CLI & service for build/rebuild/update FAISS index
│   └── translation/
│       ├── language_detector.py      # Automatic language identifier (en, kn, hi)
│       ├── cache.py                  # Database-backed translation caching
│       ├── providers/
│       │   ├── base.py               # Abstract TranslationProvider interface
│       │   ├── google_provider.py    # Google Translate provider
│       │   ├── libretranslate_provider.py # LibreTranslate API provider
│       │   └── mock_provider.py      # Deterministic Mock provider for testing/offline
│       └── translation_service.py    # Central translation service
├── api/
│   ├── routes/
│   │   ├── recommendation.py         # POST /api/ai/recommendations
│   │   ├── translation.py            # POST /api/translate & /api/festivals/{id}/translate
│   │   ├── index_mgmt.py             # GET/POST /api/ai/index/status & /rebuild
│   │   └── festivals.py              # GET/POST /api/festivals (Publish & auto-index)
│   └── main.py                       # FastAPI application entrypoint & lifespan pre-loader
└── tests/
    ├── test_embedding.py             # Sentence Transformer unit tests
    ├── test_faiss.py                 # FAISS index persistence & vector CRUD tests
    ├── test_ranking.py               # Hybrid ranking engine unit tests
    ├── test_recommendation.py        # Recommendation service integration tests
    ├── test_translation.py           # Translation provider & cache tests
    └── test_api.py                   # FastAPI REST endpoint integration tests
```

---

## Environment Configuration (`.env`)

```env
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
FAISS_INDEX_PATH=data/faiss_index.bin
FAISS_MAPPING_PATH=data/faiss_id_mapping.json

SEMANTIC_WEIGHT=0.50
LOCATION_WEIGHT=0.20
DATE_WEIGHT=0.20
CATEGORY_WEIGHT=0.10

TRANSLATION_PROVIDER=google
TRANSLATION_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./sanskriti_ai.db
```

---

## Execution Instructions

### 1. Database Initialization & Seeding
```bash
python -m database.seed
```

### 2. FAISS Vector Index Build
```bash
python -m ai.recommendation.index_manager rebuild
```

### 3. Launch FastAPI Backend
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```
Interactive OpenAPI documentation will be accessible at: `http://localhost:8000/docs`.

### 4. Run Automated Test Suite
```bash
pytest tests/ -v
```

---

## API Endpoints Specification

### Recommendations API
- **`POST /api/ai/recommendations`**
  - **Request Payload**:
    ```json
    {
      "interests": ["folk", "traditional food", "heritage"],
      "query": "I want to experience authentic village festivals and coastal food",
      "location": {
        "city": "Bengaluru",
        "latitude": 12.9716,
        "longitude": 77.5946
      },
      "start_date": "2026-10-01",
      "end_date": "2026-10-10",
      "language": "en",
      "limit": 5
    }
    ```
  - **Response Payload**:
    ```json
    {
      "success": true,
      "language": "en",
      "total_found": 5,
      "recommendations": [
        {
          "festival_id": "fest-mysuru-dasara-001",
          "festival_name": "Mysuru Dasara (Nada Habba)",
          "category": "Heritage, Cultural, Royal",
          "match_score": 93,
          "match_reason": "Strong match for your interest in Heritage and Folk.",
          "explanation_signals": [
            "You selected Heritage, Folk, Food",
            "The festival occurs during your travel period",
            "The festival is easily accessible from your location (~135 km away)"
          ],
          "location": "Mysore Palace & Chamundi Hill",
          "district": "Mysuru",
          "distance_km": 135.4,
          "start_date": "2026-10-01",
          "end_date": "2026-10-10"
        }
      ]
    }
    ```

### Multilingual Translation API
- **`POST /api/translate`**: Translates text string.
- **`POST /api/festivals/{festival_id}/translate`**: Translates structured festival fields into Kannada or Hindi.

### Festival Publishing API
- **`POST /api/festivals`**: Creates a published festival and immediately updates the FAISS vector index in real time.
