"""
YuktiAi / SanskritiPulse AI - Unified Multi-Stakeholder Core REST API
=====================================================================
Unified FastAPI application bringing together all 6 stakeholder roles:
- Member 1 (Tezraj): Core Dataset & PostgreSQL DB
- Member 2 (Nandish): AI Recommendation & Multilingual Engine
- Member 3 (Simran): Travel Planner & Hotel Engine
- Member 4 (Monika): Tourist Dashboard & Real-Time Updates
- Member 5 (Gov Analytics): Department Intelligence & Crowd Risk
- Member 6 (Tanishi): Site Operations & Broadcast Announcements
"""

import os
from pathlib import Path
from typing import Optional, List, Union, Any
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Import engines
from ai_engine import ai_engine
from travel_engine import travel_engine
from analytics_engine import analytics_engine
from organizer_engine import organizer_engine

app = FastAPI(
    title="SanskritiPulse AI - Multi-Stakeholder Unified Backend",
    version="2.0.0",
    description="Unified REST API for AI Recommendations, Multilingual Engine, Travel Planner, Gov Analytics, and Live Site Operations"
)

# ---------------------------------------------------------
# Active CORS Middleware (Allowing all origins for dashboards)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Static Files Mounting
# ---------------------------------------------------------
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# ---------------------------------------------------------
# Pydantic Request Models
# ---------------------------------------------------------
class RecommendRequest(BaseModel):
    interests: List[str] = Field(..., example=["food", "folk", "culture"])


class TranslateRequest(BaseModel):
    text: str = Field(..., example="Welcome to Mysuru Dasara festival!")
    target_lang: str = Field(..., example="kn", description="'kn', 'hi', or 'en'")


class TravelPlanRequest(BaseModel):
    origin: str = Field(..., example="Bangalore")
    festival_id: Union[str, int] = Field(..., example="mysuru-dasara")
    date: str = Field(..., example="2026-10-15")


class AnnouncementRequest(BaseModel):
    festival_id: Union[str, int] = Field(..., example="mysuru-dasara")
    message: str = Field(..., example="Jamboo Savari procession starts at 4:00 PM today!")


# ---------------------------------------------------------
# Core Health & Database Endpoints (Member 1 - Tezraj)
# ---------------------------------------------------------
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "yuktiai"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password123"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}


def get_db_connection():
    import psycopg2
    from psycopg2.extras import RealDictCursor
    return psycopg2.connect(**DB_CONFIG, connect_timeout=1, cursor_factory=RealDictCursor)


@app.get("/")
def home():
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "status": "online",
        "service": "SanskritiPulse AI Unified Multi-Stakeholder Backend",
        "version": "2.0.0",
        "modules": [
            "AI Recommendation Engine",
            "Multilingual Translation Engine",
            "Travel Route & Hotel Engine",
            "Gov Analytics & Crowd Risk Engine",
            "Organizer Site Ops & Announcement Engine"
        ]
    }


@app.get("/festivals")
def get_festivals(
    district: Optional[str] = Query(None, description="Filter festivals by district name"),
    category: Optional[str] = Query(None, description="Filter festivals by category name"),
    date: Optional[str] = Query(None, description="Filter festivals active on a specific date (YYYY-MM-DD)")
):
    """Retrieve master festivals list with optional filters."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT f.*, c.name as category_name 
            FROM festivals f
            LEFT JOIN festival_categories c ON f.category_id = c.id
            WHERE 1=1
        """
        params = []
        if district:
            query += " AND LOWER(f.district) = LOWER(%s)"
            params.append(district)
        if category:
            query += " AND LOWER(c.name) = LOWER(%s)"
            params.append(category)
        if date:
            query += " AND f.start_date <= %s AND f.end_date >= %s"
            params.extend([date, date])

        cursor.execute(query, params)
        festivals = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"count": len(festivals), "data": festivals}
    except Exception:
        # Fallback to local dataset if DB unavailable
        festivals = travel_engine.festivals
        filtered = []
        for f in festivals:
            if district and district.lower() not in str(f.get("district", "")).lower():
                continue
            if category and category.lower() not in str(f.get("category", "")).lower():
                continue
            filtered.append(f)
        return {"count": len(filtered), "data": filtered}


@app.get("/festivals/{festival_id}")
def get_festival_detail(festival_id: Union[int, str]):
    """Fetch complete detail record for a festival including images, hotels, and travel options."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.*, c.name as category 
            FROM festivals f
            LEFT JOIN festival_categories c ON f.category_id = c.id
            WHERE f.id = %s OR LOWER(f.name) LIKE %s
        """, (festival_id if isinstance(festival_id, int) and festival_id > 0 else -1, f"%{str(festival_id).replace('-', ' ')}%"))
        festival = cursor.fetchone()
        if not festival:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Festival not found")

        fid = festival["id"]
        cursor.execute("SELECT image_url FROM festival_images WHERE festival_id = %s", (fid,))
        festival["images"] = [row["image_url"] for row in cursor.fetchall()]

        cursor.execute("SELECT hotel_name, distance_km, price_per_night, booking_url FROM hotels WHERE festival_id = %s", (fid,))
        festival["hotels"] = cursor.fetchall()

        cursor.execute("SELECT mode, estimated_cost, duration FROM travel_options WHERE festival_id = %s", (fid,))
        festival["travel_options"] = cursor.fetchall()

        cursor.close()
        conn.close()
        return festival
    except HTTPException:
        raise
    except Exception:
        fest = travel_engine._find_festival(festival_id)
        if not fest:
            raise HTTPException(status_code=404, detail="Festival not found")
        return fest


# ---------------------------------------------------------
# Step 1: AI Recommendation & Multilingual Engine (Member 2 - Nandish)
# ---------------------------------------------------------
@app.post("/recommend")
def recommend_festivals(payload: RecommendRequest):
    """POST /recommend: Scores festival matches against user interest tags using Cosine Similarity."""
    results = ai_engine.recommend(payload.interests)
    return {
        "status": "success",
        "interests_submitted": payload.interests,
        "count": len(results),
        "recommendations": results
    }


@app.post("/translate")
def translate_content(payload: TranslateRequest):
    """POST /translate: Translates text content to 'kn', 'hi', or 'en'."""
    result = ai_engine.translate(payload.text, payload.target_lang)
    return result


# ---------------------------------------------------------
# Step 2: Travel Planner & Hotel Engine (Member 3 - Simran)
# ---------------------------------------------------------
@app.post("/travel-plan")
def calculate_travel_plan(payload: TravelPlanRequest):
    """POST /travel-plan: Generates transit mode comparisons and 2-day structured itinerary."""
    plan = travel_engine.generate_travel_plan(
        origin=payload.origin,
        festival_id=payload.festival_id,
        date=payload.date
    )
    return plan


@app.get("/hotels/{location}")
def get_nearby_hotels(location: str):
    """GET /hotels/{location}: Returns hotels near a district, city, or festival venue."""
    hotels_data = travel_engine.get_hotels_by_location(location)
    return hotels_data


# ---------------------------------------------------------
# Step 3: Government Analytics & Crowd Risk (Member 5)
# ---------------------------------------------------------
@app.get("/analytics/overview")
def get_analytics_overview():
    """GET /analytics/overview: Returns high-level KPI metrics across Karnataka festivals."""
    return analytics_engine.get_overview()


@app.get("/analytics/map-data")
def get_analytics_map_data():
    """GET /analytics/map-data: Returns GeoJSON-ready markers with risk levels & growth %."""
    return analytics_engine.get_map_data()


@app.get("/analytics/trends")
def get_analytics_trends():
    """GET /analytics/trends: Returns category-wise and district-wise footfall distribution data."""
    return analytics_engine.get_trends()


# ---------------------------------------------------------
# Step 4: Organizer Site Ops & Live Announcements (Member 6 - Tanishi)
# ---------------------------------------------------------
@app.get("/organizer/overview/{festival_id}")
def get_organizer_overview(festival_id: str):
    """GET /organizer/overview/{festival_id}: Real-time visitor estimates, peak hours & crowd flags."""
    return organizer_engine.get_organizer_overview(festival_id)


@app.post("/organizer/announcement")
def create_announcement(payload: AnnouncementRequest):
    """POST /organizer/announcement: Save broadcast announcement with timestamp."""
    result = organizer_engine.add_announcement(
        festival_id=payload.festival_id,
        message=payload.message
    )
    return {
        "status": "success",
        "message": "Announcement published successfully",
        "data": result
    }


@app.get("/announcements/{festival_id}")
def get_announcements(festival_id: str):
    """GET /announcements/{festival_id}: Fetch live announcements for Tourist Dashboard (Monika)."""
    return organizer_engine.get_announcements(festival_id)