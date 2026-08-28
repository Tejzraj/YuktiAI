"""
SanskritiPulse AI - Unified Modular FastAPI Main Application
"""

import os
from pathlib import Path
from typing import Optional, List, Union, Any
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Import engine modules
from database import get_db_connection
from ai_engine import ai_engine
from travel_engine import travel_engine
from analytics_engine import analytics_engine
from organizer_engine import organizer_engine

app = FastAPI(
    title="SanskritiPulse AI - Modular Full-Stack Backend",
    version="3.0.0",
    description="Unified API supporting Multi-Role Auth, AI Recommendations, Haversine Distance Travel Planner, Gov Analytics, and Organizer Event Publishing."
)

# Active CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static & Template Directories Setup
BASE_DIR = Path(__file__).resolve().parent.parent.parent
static_dir = BASE_DIR / "frontend" / "static"
templates_dir = BASE_DIR / "frontend" / "templates"
static_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Mock In-Memory User Store for Authentication
USERS_DB = {
    "tourist1": {"username": "tourist1", "password": "password123", "role": "tourist", "name": "Monika (Tourist)"},
    "organizer1": {"username": "organizer1", "password": "password123", "role": "organizer", "name": "Tanishi (Organizer)"},
    "gov1": {"username": "gov1", "password": "password123", "role": "government", "name": "Dept Analytics Officer"}
}


# ---------------------------------------------------------
# Pydantic Request Models
# ---------------------------------------------------------
class AuthRequest(BaseModel):
    username: str = Field(..., example="tourist1")
    password: str = Field(..., example="password123")
    role: Optional[str] = Field("tourist", example="tourist")


class RecommendRequest(BaseModel):
    interests: List[str] = Field(..., example=["food", "folk", "culture"])


class TranslateRequest(BaseModel):
    text: str = Field(..., example="Welcome to Mysuru Dasara festival!")
    target_lang: str = Field(..., example="kn")


class TravelPlanRequest(BaseModel):
    starting_city: Optional[str] = Field("Bangalore", example="Bangalore")
    origin: Optional[str] = Field("Bangalore", example="Bangalore")
    destination_festival: Optional[str] = Field("mysuru-dasara", example="mysuru-dasara")
    festival_id: Optional[Union[str, int]] = Field("mysuru-dasara", example="mysuru-dasara")
    start_date: Optional[str] = Field("2026-10-15", example="2026-10-15")
    date: Optional[str] = Field("2026-10-15", example="2026-10-15")
    end_date: Optional[str] = Field(None, example="2026-10-17")
    number_of_people: Optional[int] = Field(1, example=2)


class AnnouncementRequest(BaseModel):
    festival_id: Union[str, int] = Field(..., example="mysuru-dasara")
    message: str = Field(..., example="Jamboo Savari procession starts at 4:00 PM today!")


class PublishFestivalRequest(BaseModel):
    name: str = Field(..., example="Gavisiddheshwara Jatre")
    district: str = Field(..., example="Koppal")
    city: Optional[str] = Field("Koppal", example="Koppal")
    category: Optional[str] = Field("Spiritual & Folk", example="Spiritual & Folk")
    latitude: Optional[float] = Field(15.3524, example=15.3524)
    longitude: Optional[float] = Field(76.1557, example=76.1557)
    start_date: Optional[str] = Field("2026-01-15", example="2026-01-15")
    end_date: Optional[str] = Field("2026-01-18", example="2026-01-18")
    short_description: Optional[str] = Field("Massive religious congregation and fair in Koppal.", example="Massive fair.")
    expected_footfall: Optional[int] = Field(500000, example=500000)
    image_url: Optional[str] = Field("https://images.unsplash.com/photo-1600100397608-f010f443b749", example="https://images.unsplash.com/photo-1600100397608-f010f443b749")


# ---------------------------------------------------------
# Core Web UI Route
# ---------------------------------------------------------
@app.get("/")
def home():
    index_file = templates_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    fallback_index = static_dir.parent.parent / "static" / "index.html"
    if fallback_index.exists():
        return FileResponse(str(fallback_index))
    return {
        "service": "SanskritiPulse AI Multi-Stakeholder Unified Backend",
        "status": "online",
        "version": "3.0.0"
    }


# ---------------------------------------------------------
# Multi-Role Authentication Endpoints (Step 3)
# ---------------------------------------------------------
@app.post("/auth/register")
def register_user(payload: AuthRequest):
    """Register a new user with role ('tourist', 'organizer', 'government')."""
    if payload.username in USERS_DB:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    USERS_DB[payload.username] = {
        "username": payload.username,
        "password": payload.password,
        "role": payload.role or "tourist",
        "name": payload.username.capitalize()
    }
    return {
        "status": "success",
        "message": f"Account created for {payload.username} with role {payload.role}",
        "user": {
            "username": payload.username,
            "role": payload.role
        }
    }


@app.post("/auth/login")
def login_user(payload: AuthRequest):
    """Authenticate user and return role token & profile."""
    user = USERS_DB.get(payload.username)
    if not user or user["password"] != payload.password:
        # Default tourist login fallback for smooth demo testing
        return {
            "status": "success",
            "message": "Authenticated as Guest Tourist",
            "token": "token_guest_tourist",
            "user": {
                "username": payload.username,
                "role": payload.role or "tourist",
                "name": payload.username
            }
        }
    return {
        "status": "success",
        "message": "Login successful",
        "token": f"token_{user['username']}",
        "user": {
            "username": user["username"],
            "role": user["role"],
            "name": user.get("name", user["username"])
        }
    }


# ---------------------------------------------------------
# Core Master Dataset Endpoints
# ---------------------------------------------------------
@app.get("/festivals")
def get_festivals(
    district: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    date: Optional[str] = Query(None)
):
    """Retrieve master festivals list."""
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
def get_festival_detail(festival_id: str):
    """Fetch detail record for a festival."""
    fest = travel_engine._find_festival(festival_id)
    if not fest:
        raise HTTPException(status_code=404, detail="Festival not found")
    return fest


# ---------------------------------------------------------
# Step 1: AI Recommendation & Multilingual Engine
# ---------------------------------------------------------
@app.post("/recommend")
def recommend_festivals(payload: RecommendRequest):
    """POST /recommend: Scores matches against user interests."""
    results = ai_engine.recommend(payload.interests)
    return {
        "status": "success",
        "interests_submitted": payload.interests,
        "count": len(results),
        "recommendations": results
    }


@app.post("/translate")
def translate_content(payload: TranslateRequest):
    """POST /translate: Translates text content."""
    return ai_engine.translate(payload.text, payload.target_lang)


# ---------------------------------------------------------
# Step 2 & 5: Travel Planner, Hotels & Interactive Tourist Guide
# ---------------------------------------------------------
@app.post("/travel-plan")
def calculate_travel_plan(payload: TravelPlanRequest):
    """POST /travel-plan: Calculates Haversine distance, budget, transit comparisons, and 2-day itinerary."""
    city = payload.starting_city or payload.origin or "Bangalore"
    fest = payload.destination_festival or payload.festival_id or "mysuru-dasara"
    s_date = payload.start_date or payload.date or "2026-10-15"
    people = payload.number_of_people or 1

    return travel_engine.calculate_travel_plan(
        starting_city=city,
        destination_festival=fest,
        start_date=s_date,
        end_date=payload.end_date,
        number_of_people=people
    )


@app.get("/hotels/{location}")
def get_nearby_hotels(location: str):
    """GET /hotels/{location}: Returns hotels near a location."""
    return travel_engine.get_hotels_by_location(location)


@app.get("/tourist-guide/{festival_id}")
def get_tourist_guide(festival_id: str):
    """GET /tourist-guide/{festival_id}: Returns rich interactive AI Tourist Guide modal content."""
    fest = travel_engine._find_festival(festival_id)
    if not fest:
        fest = {
            "name": festival_id.replace("-", " ").title(),
            "cultural_significance": "Rich cultural heritage festival of Karnataka.",
            "history_origin": "Historical tradition preserved across generations.",
            "major_attractions": ["Grand Procession", "Illumination", "Cultural Stage Performances"],
            "local_food": ["Mysore Pak", "Masala Dosa", "Filter Coffee"],
            "best_time_to_visit": "October - November",
            "dos_and_donts": {
                "dos": ["Respect temple traditions", "Wear comfortable footwear"],
                "donts": ["Do not litter venue grounds", "Avoid flash photography near sacred idols"]
            }
        }

    return {
        "festival_id": festival_id,
        "name": fest.get("name"),
        "what_is_it": fest.get("short_description") or "Living cultural festival of Karnataka.",
        "why_celebrated": fest.get("cultural_significance") or "Celebrates regional heritage, victory of good over evil, and community harmony.",
        "history_origin": fest.get("history_origin") or "Practiced historically for centuries across Karnataka.",
        "what_tourists_will_see": fest.get("major_attractions") or ["Grand Processions", "Cultural Shows"],
        "local_food_recommendations": fest.get("local_food") or ["Mysore Pak", "Masala Dosa"],
        "best_time_to_visit": fest.get("best_time_to_visit") or "Festival Dates & Evening Ceremonies",
        "cultural_etiquette": fest.get("dos_and_donts") or {
            "dos": ["Wear modest attire inside temples", "Keep venue clean"],
            "donts": ["Do not touch ancient monuments", "Avoid single-use plastics"]
        }
    }


# ---------------------------------------------------------
# Step 3 & 4: Gov Analytics & Organizer Site Ops Publishing
# ---------------------------------------------------------
@app.get("/analytics/overview")
def get_analytics_overview():
    return analytics_engine.get_overview()


@app.get("/analytics/map-data")
def get_analytics_map_data():
    return analytics_engine.get_map_data()


@app.get("/analytics/trends")
def get_analytics_trends():
    return analytics_engine.get_trends()


@app.get("/organizer/overview/{festival_id}")
def get_organizer_overview(festival_id: str):
    return organizer_engine.get_organizer_overview(festival_id)


@app.post("/organizer/announcement")
def create_announcement(payload: AnnouncementRequest):
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
    return organizer_engine.get_announcements(festival_id)


@app.post("/organizer/publish-festival")
def publish_festival(payload: PublishFestivalRequest):
    """POST /organizer/publish-festival: Organizer publishes a new festival directly to live tourist feed and map markers."""
    fest_dict = payload.dict()
    result = organizer_engine.publish_new_festival(fest_dict)

    # Append to travel_engine memory
    new_fest = result["festival"]
    travel_engine.festivals.insert(0, new_fest)
    ai_engine.festivals.insert(0, new_fest)
    analytics_engine.festivals.insert(0, new_fest)

    return result
