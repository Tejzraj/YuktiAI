#!/usr/bin/env python3
"""
SanskritiPulse - PostgreSQL Database Seeding Script
===================================================
Seeds festival categories, festivals master, images, hotels, and travel options
from JSON dataset into the PostgreSQL database.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
def get_psycopg2():
    try:
        import psycopg2
        return psycopg2
    except ImportError:
        sys.exit(
            "❌ Error: 'psycopg2' is not installed.\n"
            "   Please install it using: pip install psycopg2-binary"
        )

# Default DB Configuration (matches docker-compose.yml & environment variables)
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "sanskritipulse"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password123"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}


def find_default_json_file() -> Optional[Path]:
    """Search for the festival JSON dataset in standard workspace locations."""
    script_dir = Path(__file__).resolve().parent
    candidates = [
        script_dir / "festivals_karnataka.json",
        script_dir / "sanskritipulse-ai" / "festivals_karnataka.json",
        script_dir / "mock_festivals.json",
        Path.cwd() / "festivals_karnataka.json",
        Path.cwd() / "sanskritipulse-ai" / "festivals_karnataka.json",
        Path.cwd() / "mock_festivals.json",
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def get_category_id(cursor, category_name: str) -> int:
    """Get existing category ID or insert a new category and return its ID."""
    # Ensure category name fits VARCHAR(50)
    trimmed_name = (category_name or "General")[:50].strip()
    cursor.execute(
        """
        INSERT INTO festival_categories (name)
        VALUES (%s)
        ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
        RETURNING id;
        """,
        (trimmed_name,)
    )
    res = cursor.fetchone()
    return res[0]


def seed_database(json_path: Path, reset_tables: bool = False) -> None:
    """Loads and seeds festival data into PostgreSQL."""
    if not json_path.exists():
        raise FileNotFoundError(f"JSON data file not found: {json_path}")

    print(f"📖 Reading dataset from: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        festivals_data: List[Dict[str, Any]] = json.load(f)

    if not isinstance(festivals_data, list):
        raise ValueError("Root JSON element must be a list of festival objects.")

    psycopg2 = get_psycopg2()
    print(f"🔌 Connecting to PostgreSQL at {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}...")
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        with conn:
            with conn.cursor() as cursor:
                if reset_tables:
                    print("🧹 Truncating existing tables...")
                    cursor.execute(
                        """
                        TRUNCATE TABLE hotels, travel_options, festival_images, festivals, festival_categories 
                        RESTART IDENTITY CASCADE;
                        """
                    )

                print(f"🚀 Inserting {len(festivals_data)} festivals and related entities...")
                inserted_festivals = 0
                inserted_images = 0
                inserted_hotels = 0
                inserted_travel = 0

                for fest in festivals_data:
                    # 1. Category Resolution
                    cat_name = fest.get("category", "General")
                    category_id = get_category_id(cursor, cat_name)

                    # 2. Normalize Festival Master Fields
                    name = fest.get("name", "").strip()
                    if not name:
                        continue

                    local_name = fest.get("local_name")
                    district = fest.get("district", "Karnataka")
                    city = fest.get("city")
                    latitude = fest.get("latitude") or fest.get("lat")
                    longitude = fest.get("longitude") or fest.get("lng")
                    start_date = fest.get("start_date")
                    end_date = fest.get("end_date")
                    timings = fest.get("timings", "All Day")
                    short_desc = fest.get("short_description") or fest.get("description")
                    significance = fest.get("cultural_significance")
                    history = fest.get("history_origin") or fest.get("history")
                    attractions = fest.get("major_attractions") or fest.get("attractions") or []
                    food = fest.get("local_food") or []
                    activities = fest.get("activities") or fest.get("tags") or []
                    footfall = fest.get("expected_footfall") or fest.get("footfall")
                    website = fest.get("official_website") or fest.get("website")

                    # Check if festival already exists by name
                    cursor.execute("SELECT id FROM festivals WHERE name = %s LIMIT 1;", (name,))
                    existing = cursor.fetchone()

                    if existing:
                        festival_id = existing[0]
                        # Update master record
                        cursor.execute(
                            """
                            UPDATE festivals SET
                                local_name = %s, district = %s, city = %s,
                                latitude = %s, longitude = %s, start_date = %s, end_date = %s,
                                timings = %s, category_id = %s, short_description = %s,
                                cultural_significance = %s, history_origin = %s,
                                major_attractions = %s, local_food = %s, activities = %s,
                                expected_footfall = %s, official_website = %s
                            WHERE id = %s;
                            """,
                            (
                                local_name, district, city, latitude, longitude, start_date, end_date,
                                timings, category_id, short_desc, significance, history,
                                attractions, food, activities, footfall, website, festival_id
                            )
                        )
                    else:
                        # Insert new festival record
                        cursor.execute(
                            """
                            INSERT INTO festivals (
                                name, local_name, district, city, latitude, longitude,
                                start_date, end_date, timings, category_id, short_description,
                                cultural_significance, history_origin, major_attractions,
                                local_food, activities, expected_footfall, official_website
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                            ) RETURNING id;
                            """,
                            (
                                name, local_name, district, city, latitude, longitude,
                                start_date, end_date, timings, category_id, short_desc,
                                significance, history, attractions, food, activities,
                                footfall, website
                            )
                        )
                        festival_id = cursor.fetchone()[0]
                        inserted_festivals += 1

                    # 3. Handle Images
                    image_urls = []
                    if "images" in fest and isinstance(fest["images"], list):
                        for img in fest["images"]:
                            if isinstance(img, dict) and "url" in img:
                                image_urls.append(img["url"])
                            elif isinstance(img, str):
                                image_urls.append(img)
                    elif "image_url" in fest and fest["image_url"]:
                        image_urls.append(fest["image_url"])

                    for img_url in image_urls:
                        cursor.execute(
                            """
                            INSERT INTO festival_images (festival_id, image_url)
                            VALUES (%s, %s);
                            """,
                            (festival_id, img_url)
                        )
                        inserted_images += 1

                    # 4. Handle Hotels
                    hotels = fest.get("nearby_hotels") or fest.get("hotels") or []
                    for h in hotels:
                        h_name = h.get("name") or h.get("hotel_name")
                        h_dist = h.get("distance_km")
                        h_price = h.get("price_per_night")
                        h_url = h.get("booking_url")
                        if h_name:
                            cursor.execute(
                                """
                                INSERT INTO hotels (festival_id, hotel_name, distance_km, price_per_night, booking_url)
                                VALUES (%s, %s, %s, %s, %s);
                                """,
                                (festival_id, h_name, h_dist, h_price, h_url)
                            )
                            inserted_hotels += 1

                    # 5. Handle Travel Options
                    travel_opts = fest.get("travel_options") or fest.get("travel") or []
                    for t in travel_opts:
                        mode = t.get("mode")
                        cost = t.get("estimated_cost") or t.get("cost")
                        duration = t.get("duration")
                        if mode:
                            cursor.execute(
                                """
                                INSERT INTO travel_options (festival_id, mode, estimated_cost, duration)
                                VALUES (%s, %s, %s, %s);
                                """,
                                (festival_id, mode, cost, duration)
                            )
                            inserted_travel += 1

        print("\n✅ Database Seeding Completed Successfully!")
        print(f"   • Festivals Seeded/Updated: {len(festivals_data)} (New: {inserted_festivals})")
        print(f"   • Images Inserted: {inserted_images}")
        print(f"   • Hotels Inserted: {inserted_hotels}")
        print(f"   • Travel Options Inserted: {inserted_travel}")

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}", file=sys.stderr)
        raise
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Seed SanskritiPulse PostgreSQL database.")
    parser.add_argument(
        "-f", "--file",
        dest="json_file",
        type=Path,
        default=None,
        help="Path to festival JSON dataset (defaults to auto-detecting festivals_karnataka.json or mock_festivals.json)"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Truncate existing tables before seeding"
    )

    args = parser.parse_args()

    target_file = args.json_file or find_default_json_file()
    if not target_file:
        print("❌ Error: No JSON dataset file found. Specify one with --file <path>", file=sys.stderr)
        sys.exit(1)

    seed_database(target_file, reset_tables=args.reset)


if __name__ == "__main__":
    main()