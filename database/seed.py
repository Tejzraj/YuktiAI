#!/usr/bin/env python3
"""
SanskritiPulse AI - Database Seeding Script
"""
import os
import sys
import json
from pathlib import Path

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "sanskritipulse"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password123"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "connect_timeout": 3
}


def seed_database():
    json_path = Path(__file__).parent / "mock_festivals.json"
    if not json_path.exists():
        json_path = Path(__file__).parent.parent / "yuktiai" / "festivals_karnataka.json"

    if not json_path.exists():
        print("❌ Dataset json file not found for seeding.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        import psycopg2
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print(f"📖 Seeding {len(data)} festivals into PostgreSQL...")
        for fest in data:
            cat_name = fest.get("category", "General")[:50]
            cursor.execute("INSERT INTO festival_categories (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (cat_name,))
            cursor.execute("SELECT id FROM festival_categories WHERE name = %s;", (cat_name,))
            cat_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO festivals (
                    festival_id, name, local_name, district, city, latitude, longitude,
                    start_date, end_date, timings, category_id, short_description,
                    cultural_significance, history_origin, major_attractions, local_food,
                    activities, expected_footfall
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) ON CONFLICT (festival_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    expected_footfall = EXCLUDED.expected_footfall;
            """, (
                fest.get("id"), fest.get("name"), fest.get("local_name"), fest.get("district"),
                fest.get("city"), fest.get("latitude"), fest.get("longitude"),
                fest.get("start_date"), fest.get("end_date"), fest.get("timings"), cat_id,
                fest.get("short_description"), fest.get("cultural_significance"),
                fest.get("history_origin"), fest.get("major_attractions"), fest.get("local_food"),
                fest.get("activities"), fest.get("expected_footfall")
            ))

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database seeding completed successfully!")
    except Exception as e:
        print(f"⚠️ Seeding warning / skipped DB (using offline JSON fallback): {e}")


if __name__ == "__main__":
    seed_database()
