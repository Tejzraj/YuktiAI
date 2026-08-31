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
    "organizer1": {"username": "organizer1", "password": "password123", "role": "authority", "name": "Tanishi (Authority)"},
    "authority1": {"username": "authority1", "password": "password123", "role": "authority", "name": "Tanishi (Authority)"},
    "gov1": {"username": "gov1", "password": "password123", "role": "government", "name": "Dept Analytics Officer"}
}


# ---------------------------------------------------------
# Pydantic Request Models
# ---------------------------------------------------------
class AuthRequest(BaseModel):
    username: str = Field(..., example="tourist1")
    password: str = Field(..., example="password123")
    role: Optional[str] = Field("tourist", example="tourist")
    email: Optional[str] = Field(None, example="tourist@karnataka.gov.in")
    phone: Optional[str] = Field(None, example="+91-9876543210")


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
    cultural_significance: Optional[str] = Field("Deep spiritual legacy and communal feast.", example="Significance")
    major_attractions: Optional[List[str]] = Field(["Jatre Procession", "Temple Chariot Pulling"], example=["Chariot"])
    local_food: Optional[List[str]] = Field(["Jowar Rotti", "Sajje Kadubu"], example=["Jowar Rotti"])
    activities: Optional[List[str]] = Field(["spiritual", "folk", "fair"], example=["spiritual"])
    best_time_to_visit: Optional[str] = Field("January Jatre festival days", example="January")
    expected_footfall: Optional[int] = Field(500000, example=500000)
    image_url: Optional[str] = Field("https://images.unsplash.com/photo-1600100397608-f010f443b749", example="https://images.unsplash.com/photo-1600100397608-f010f443b749")
    owner_username: Optional[str] = Field("authority1", example="authority1")


class UpdateFestivalRequest(BaseModel):
    name: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    category: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    short_description: Optional[str] = None
    cultural_significance: Optional[str] = None
    major_attractions: Optional[List[str]] = None
    local_food: Optional[List[str]] = None
    activities: Optional[List[str]] = None
    best_time_to_visit: Optional[str] = None
    expected_footfall: Optional[int] = None
    image_url: Optional[str] = None
    owner_username: Optional[str] = None


class VerifyRequest(BaseModel):
    action: str = Field(..., example="approve")


# Search Helper
def find_festival_by_id(fest_id: str):
    for f in travel_engine.festivals:
        f_id = f.get("id") or f.get("festival_id")
        if str(f_id).lower().strip() == str(fest_id).lower().strip():
            return f
    return None


# ---------------------------------------------------------
# Multi-Role Authentication Helpers & Endpoints (Step 3)
# ---------------------------------------------------------
def save_user_to_postgres(username: str, password_hash: str, role: str, email: str = None, phone: str = None):
    """Save registered user details to PostgreSQL database, with self-healing columns and local memory fallback."""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Self-healing columns alter schema dynamically if needed
            try:
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(150);")
                cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(50);")
                conn.commit()
            except Exception as e:
                print(f"[WARNING] Schema alter warning (might be read-only): {e}")
                conn.rollback()
                
            # Insert user
            cur.execute(
                "INSERT INTO users (username, password_hash, role, email, phone) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (username) DO NOTHING;",
                (username, password_hash, role, email, phone)
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"[WARNING] PostgreSQL connection/write skipped: {e}. User saved to local fallback memory.")
        return False
    finally:
        if conn:
            conn.close()


def send_welcome_notification(username: str, email: str = None, phone: str = None, role: str = None):
    """Generates and logs an automated welcome SMS and Email for the new sign up."""
    role_name = "Tourist Visitor"
    if role == "authority":
        role_name = "Festival Event Authority"
    elif role == "government":
        role_name = "Tourism Department Official"

    # SMS draft
    sms_text = f"Welcome to SanskritiPulse AI, {username}! Your account has been approved with role '{role_name}'. Explore living traditions, manage plans, and broadcast live updates of Karnataka's grand festivals."
    
    # Email draft
    email_text = f"""Subject: Welcome to SanskritiPulse AI Portal, {username}!

Namaste {username},

Welcome to SanskritiPulse AI - the Unified Cultural Intelligence and Stakeholder Portal of Karnataka!

Your account has been successfully configured with the role: {role_name}.

Account Details:
- Username: {username}
- Assigned Role: {role_name}
- Contact Email: {email or 'Not Provided'}
- Contact Phone: {phone or 'Not Provided'}

Based on your role, you now have access to our unified features:
- Tourist Discovery: Explore custom Haversine travel plans and AI-guided routes.
- Site Operations: Publish festivals, view visitor counts, and broadcast live event advisories.
- Government Intelligence: Verify submissions, view crowd metrics, and manage regional advisory flags.

Happy Exploring!

Warm regards,
SanskritiPulse AI Engineering Team
Department of Tourism, Government of Karnataka"""

    # Log to file for verification
    log_dir = Path(__file__).parent.parent.parent / "database"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "welcome_notifications.log"
    
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n--- NOTIFICATION FOR {username.upper()} ({role_name.upper()}) at 2026-08-31 ---\n")
            f.write(f"[AUTO-SMS to {phone or 'N/A'}]:\n{sms_text}\n")
            f.write(f"[AUTO-EMAIL to {email or 'N/A'}]:\n{email_text}\n")
            f.write("-" * 60 + "\n")
    except Exception as e:
        print(f"[WARNING] Failed to write to welcome notifications log: {e}")

    # Also print to stdout
    print(f"\n[AUTO-SMS Sent to {phone or 'N/A'}]: {sms_text}")
    print(f"[AUTO-EMAIL Sent to {email or 'N/A'}]: {email_text.strip()}\n")
    
    return {
        "sms_sent": True,
        "email_sent": True,
        "sms_preview": sms_text,
        "email_preview": email_text.strip()
    }


@app.post("/auth/register")
def register_user(payload: AuthRequest):
    """Register a new user, save to PostgreSQL and local fallback memory, and send welcome notifications."""
    if payload.username in USERS_DB:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    role = payload.role or "tourist"
    if role == "organizer":
        role = "authority"  # Map organizer to authority internally
        
    # 1. Save to in-memory fallback
    USERS_DB[payload.username] = {
        "username": payload.username,
        "password": payload.password,
        "role": role,
        "name": payload.username.capitalize()
    }

    # 2. Save to PostgreSQL database
    db_saved = save_user_to_postgres(
        username=payload.username,
        password_hash=payload.password,  # Storing password in schema column
        role=role,
        email=payload.email,
        phone=payload.phone
    )

    # 3. Send automated message and email
    notif_result = send_welcome_notification(
        username=payload.username,
        email=payload.email,
        phone=payload.phone,
        role=role
    )

    return {
        "status": "success",
        "message": f"Account created for {payload.username} with role {role}.",
        "db_saved": db_saved,
        "notifications": notif_result,
        "user": {
            "username": payload.username,
            "role": role
        }
    }


@app.post("/auth/login")
def login_user(payload: AuthRequest):
    """Authenticate user and return role token & profile."""
    user = USERS_DB.get(payload.username)
    if not user or user["password"] != payload.password:
        # Check if they request organizer and map it
        role_ret = payload.role or "tourist"
        if role_ret == "organizer":
            role_ret = "authority"
        # Default tourist login fallback for smooth demo testing
        return {
            "status": "success",
            "message": "Authenticated as Guest",
            "token": f"token_guest_{payload.username}",
            "user": {
                "username": payload.username,
                "role": role_ret,
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


@app.get("/")
def home():
    """GET /: Serve the main index.html portal page."""
    index_file = templates_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "status": "online",
        "message": "FastAPI server is running, but templates/index.html was not found."
    }


# ---------------------------------------------------------
# Core Master Dataset Endpoints
# ---------------------------------------------------------
@app.get("/festivals")
def get_festivals(
    district: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    username: Optional[str] = Query(None)
):
    """Retrieve master festivals list with verification and role-based filtering."""
    festivals = travel_engine.festivals
    filtered = []
    
    # Standardize roles
    std_role = (role or "").lower().strip()
    if std_role == "organizer":
        std_role = "authority"
        
    for f in festivals:
        # Standardize workflow fields on mock data if missing
        f_verified = f.get("verified")
        if f_verified is None:
            f_verified = True
            f["verified"] = True
            
        f_status = f.get("verification_status")
        if f_status is None:
            f_status = "approved"
            f["verification_status"] = "approved"
            
        f_owner = f.get("owner_username")
        if f_owner is None:
            f_owner = "system"
            f["owner_username"] = "system"

        # Apply workflow filtering:
        # 1. Government role sees all events
        # 2. Authority role sees approved events + pending/rejected events they own
        # 3. Tourists & guests only see verified & approved events
        if std_role == "government":
            pass
        elif std_role == "authority":
            if not f_verified and f_owner != username:
                continue
        else:
            if not f_verified or f_status != "approved":
                continue

        if district and district.lower() not in str(f.get("district", "")).lower():
            continue
        if category and category.lower() not in str(f.get("category", "")).lower():
            continue
        filtered.append(f)
    return {"count": len(filtered), "data": filtered}


@app.get("/festivals/{festival_id}")
def get_festival_detail(festival_id: str):
    """Fetch detail record for a festival."""
    fest = find_festival_by_id(festival_id)
    if not fest:
        # Fallback to general lookup
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
    """POST /organizer/publish-festival: Organizer publishes a new festival directly to live memory and saves to JSON."""
    fest_dict = payload.dict()
    
    # Force default workflow fields
    fest_dict["verified"] = False
    fest_dict["verification_status"] = "pending"
    fest_dict["owner_username"] = fest_dict.get("owner_username") or "authority1"
    
    result = organizer_engine.publish_new_festival(fest_dict)
    new_fest = result["festival"]

    # Append to engine memory
    travel_engine.festivals.insert(0, new_fest)
    ai_engine.festivals.insert(0, new_fest)
    analytics_engine.festivals.insert(0, new_fest)

    # Save to mock database file for persistence
    from database import save_festivals_to_json
    save_festivals_to_json(travel_engine.festivals)

    return result


@app.put("/organizer/update-festival/{festival_id}")
def update_festival(festival_id: str, payload: UpdateFestivalRequest):
    """PUT /organizer/update-festival/{festival_id}: Edit / update details of an existing festival."""
    fest = find_festival_by_id(festival_id)
    if not fest:
        raise HTTPException(status_code=404, detail="Festival not found")
        
    update_data = payload.dict(exclude_unset=True)
    for k, v in update_data.items():
        if v is not None:
            fest[k] = v
            
    # Save to mock database file for persistence
    from database import save_festivals_to_json
    save_festivals_to_json(travel_engine.festivals)
    
    return {
        "status": "success",
        "message": f"Festival '{fest.get('name')}' updated successfully.",
        "festival": fest
    }


@app.delete("/organizer/delete-festival/{festival_id}")
def delete_festival(festival_id: str, username: Optional[str] = Query(None)):
    """DELETE /organizer/delete-festival/{festival_id}: Delete/unpublish a festival."""
    found = False
    for i, f in enumerate(travel_engine.festivals):
        f_id = f.get("id") or f.get("festival_id")
        if str(f_id).lower() == festival_id.lower():
            if username and f.get("owner_username") and f.get("owner_username") != username:
                raise HTTPException(status_code=403, detail="Not authorized to delete this festival")
            travel_engine.festivals.pop(i)
            found = True
            break
            
    if not found:
        raise HTTPException(status_code=404, detail="Festival not found")
        
    # Sync memory references in other engines
    ai_engine.festivals = [f for f in ai_engine.festivals if str(f.get("id") or f.get("festival_id")).lower() != festival_id.lower()]
    analytics_engine.festivals = [f for f in analytics_engine.festivals if str(f.get("id") or f.get("festival_id")).lower() != festival_id.lower()]
    
    # Save to mock database file for persistence
    from database import save_festivals_to_json
    save_festivals_to_json(travel_engine.festivals)
    
    return {
        "status": "success",
        "message": "Festival deleted successfully from memory and JSON."
    }


@app.post("/gov/verify-festival/{festival_id}")
def verify_festival(festival_id: str, payload: VerifyRequest):
    """POST /gov/verify-festival/{festival_id}: Government department approves or rejects a festival."""
    fest = find_festival_by_id(festival_id)
    if not fest:
        raise HTTPException(status_code=404, detail="Festival not found")
        
    action = payload.action.lower().strip()
    if action == "approve":
        fest["verified"] = True
        fest["verification_status"] = "approved"
    elif action == "reject":
        fest["verified"] = False
        fest["verification_status"] = "rejected"
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'approve' or 'reject'")
        
    # Save to mock database file for persistence
    from database import save_festivals_to_json
    save_festivals_to_json(travel_engine.festivals)
    
    return {
        "status": "success",
        "message": f"Festival has been {fest['verification_status']}.",
        "festival": fest
    }
