from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="SanskritiPulse Core Festival API", version="1.0.0")

DB_CONFIG = {
    "dbname": "sanskritipulse",
    "user": "postgres",
    "password": "password123",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

@app.get("/")
def home():
    return {"status": "online", "message": "SanskritiPulse Core Database API running"}

@app.get("/festivals")
def get_festivals(
    district: Optional[str] = None,
    category: Optional[str] = None,
    date: Optional[str] = None
):
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

@app.get("/festivals/{festival_id}")
def get_festival_detail(festival_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT f.*, c.name as category 
        FROM festivals f
        LEFT JOIN festival_categories c ON f.category_id = c.id
        WHERE f.id = %s
    """, (festival_id,))
    
    festival = cursor.fetchone()
    if not festival:
        conn.close()
        raise HTTPException(status_code=404, detail="Festival not found")

    # Fetch images
    cursor.execute("SELECT image_url FROM festival_images WHERE festival_id = %s", (festival_id,))
    festival["images"] = [row["image_url"] for row in cursor.fetchall()]

    # Fetch hotels
    cursor.execute("SELECT hotel_name, distance_km, price_per_night FROM hotels WHERE festival_id = %s", (festival_id,))
    festival["hotels"] = cursor.fetchall()

    cursor.close()
    conn.close()
    return festival