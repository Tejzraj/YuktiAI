"""
YuktiAI - Travel Planner & Hotel Engine
Member 3: Simran
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Union, Optional

# Major Karnataka hubs coordinates (lat, lng)
HUB_COORDINATES = {
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "mysuru": (12.2958, 76.6394),
    "mysore": (12.2958, 76.6394),
    "mangaluru": (12.9141, 74.8560),
    "mangalore": (12.9141, 74.8560),
    "hubballi": (15.3647, 75.1240),
    "hubli": (15.3647, 75.1240),
    "belagavi": (15.8497, 74.4977),
    "belgaum": (15.8497, 74.4977),
}

# Precalculated road distances (in km) between major hubs and key Karnataka destinations
DIST_MATRIX = {
    ("bangalore", "mysuru"): 145,
    ("bangalore", "mangaluru"): 350,
    ("bangalore", "hubballi"): 410,
    ("bangalore", "belagavi"): 500,
    ("bangalore", "vijayanagara"): 340,
    ("bangalore", "hampi"): 340,
    ("bangalore", "udupi"): 400,
    ("bangalore", "kodagu"): 250,
    ("bangalore", "coorg"): 250,
    ("bangalore", "kalaburagi"): 570,
    ("bangalore", "bidar"): 690,
    ("mysuru", "mangaluru"): 255,
    ("mysuru", "hubballi"): 450,
    ("hubballi", "belagavi"): 95,
}

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "yuktiai"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password123"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}


def load_festivals() -> List[Dict[str, Any]]:
    """Load festivals from PostgreSQL database or JSON dataset fallback."""
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.id, f.name, f.district, f.city, f.latitude as lat, f.longitude as lng,
                   f.timings, f.short_description, f.major_attractions, f.local_food,
                   c.name as category
            FROM festivals f
            LEFT JOIN festival_categories c ON f.category_id = c.id
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows:
            return [dict(r) for r in rows]
    except Exception:
        pass

    candidates = [
        Path(__file__).parent / "yuktiai" / "festivals_karnataka.json",
        Path(__file__).parent / "festivals_karnataka.json",
        Path.cwd() / "yuktiai" / "festivals_karnataka.json",
        Path.cwd() / "festivals_karnataka.json",
    ]
    for p in candidates:
        if p.is_file():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

    return [
        {
            "id": "mysuru-dasara",
            "name": "Mysuru Dasara",
            "district": "Mysuru",
            "city": "Mysuru",
            "lat": 12.3051,
            "lng": 76.6551,
            "timings": "9:00 AM - 10:00 PM",
            "category": "State Festival & Royal Heritage"
        },
        {
            "id": "hampi-utsav",
            "name": "Hampi Utsav",
            "district": "Vijayanagara",
            "city": "Hampi",
            "lat": 15.3350,
            "lng": 76.4600,
            "timings": "10:00 AM - 11:00 PM",
            "category": "Heritage & Culture"
        },
        {
            "id": "kambala-race",
            "name": "Kambala Buffalo Race",
            "district": "Dakshina Kannada",
            "city": "Mangaluru",
            "lat": 12.9141,
            "lng": 74.8560,
            "timings": "8:00 AM - 8:00 PM",
            "category": "Folk & Sports"
        }
    ]


class TravelEngine:
    def __init__(self):
        self.festivals = load_festivals()

    def _find_festival(self, fest_id_or_name: Union[str, int]) -> Optional[Dict[str, Any]]:
        target_str = str(fest_id_or_name).lower().strip()
        for f in self.festivals:
            f_id = str(f.get("id", "")).lower()
            f_name = str(f.get("name", "")).lower()
            if target_str in [f_id, f_name] or target_str in f_id or f_id in target_str or target_str in f_name:
                return f
        return self.festivals[0] if self.festivals else None

    def _estimate_distance(self, origin: str, dest_district: str) -> float:
        orig_key = origin.lower().strip()
        dest_key = dest_district.lower().strip()

        if (orig_key, dest_key) in DIST_MATRIX:
            return float(DIST_MATRIX[(orig_key, dest_key)])
        if (dest_key, orig_key) in DIST_MATRIX:
            return float(DIST_MATRIX[(dest_key, orig_key)])

        # Default fallback distance estimation
        return 220.0

    def generate_travel_plan(self, origin: str, festival_id: Union[str, int], date: str) -> Dict[str, Any]:
        fest = self._find_festival(festival_id)
        fest_name = fest.get("name", "Festival") if fest else "Karnataka Festival"
        dest_district = fest.get("district", "Karnataka") if fest else "Karnataka"
        dest_city = fest.get("city", dest_district) if fest else dest_district
        timings = fest.get("timings", "All Day") if fest else "All Day"

        distance_km = self._estimate_distance(origin, dest_district)

        # Calculate transit modes
        # Bus: ~50 km/h, ₹2.2/km
        bus_hrs = max(1.5, round(distance_km / 50.0, 1))
        bus_cost = int(distance_km * 2.2)

        # Train: ~60 km/h, ₹1.5/km
        train_hrs = max(1.2, round(distance_km / 60.0, 1))
        train_cost = int(distance_km * 1.5)

        # Car: ~75 km/h, ₹8.0/km
        car_hrs = max(1.0, round(distance_km / 75.0, 1))
        car_cost = int(distance_km * 8.0)

        mode_comparisons = [
            {
                "mode": "Bus",
                "duration": f"{bus_hrs} hours",
                "estimated_cost": f"₹{bus_cost}",
                "distance_km": distance_km,
                "comfort_rating": "4.2/5",
                "recommended_for": "Budget Travelers & Frequent Buses"
            },
            {
                "mode": "Train",
                "duration": f"{train_hrs} hours",
                "estimated_cost": f"₹{train_cost}",
                "distance_km": distance_km,
                "comfort_rating": "4.5/5",
                "recommended_for": "Scenic Journey & Maximum Comfort"
            },
            {
                "mode": "Car (Private / Taxi)",
                "duration": f"{car_hrs} hours",
                "estimated_cost": f"₹{car_cost}",
                "distance_km": distance_km,
                "comfort_rating": "4.8/5",
                "recommended_for": "Families & Flexible Schedule"
            }
        ]

        # 2-Day Structured Itinerary
        itinerary_day1 = {
            "day": 1,
            "title": f"Arrival in {dest_city} & Evening Festival Experience",
            "schedule": [
                {
                    "time": "07:00 AM - 11:30 AM",
                    "activity": f"Depart from {origin} to {dest_city} via selected transport ({car_hrs} - {bus_hrs} hrs journey)."
                },
                {
                    "time": "12:00 PM - 01:30 PM",
                    "activity": f"Check-in at pre-booked hotel in {dest_city}, freshen up & enjoy authentic local lunch."
                },
                {
                    "time": "02:30 PM - 05:30 PM",
                    "activity": f"Visit {fest_name} main venue. Explore cultural exhibitions, stalls, and heritage displays."
                },
                {
                    "time": "06:00 PM - 09:30 PM",
                    "activity": f"Witness grand evening cultural performances, lighting ceremonies ({timings})."
                },
                {
                    "time": "09:30 PM Onwards",
                    "activity": f"Traditional dinner featuring regional specialties and return to hotel."
                }
            ]
        }

        itinerary_day2 = {
            "day": 2,
            "title": f"Local Heritage Tour & Grand Procession",
            "schedule": [
                {
                    "time": "08:00 AM - 10:00 AM",
                    "activity": f"Breakfast with regional delicacies (Dosa, Vada, filter coffee) & visit nearby landmarks."
                },
                {
                    "time": "10:30 AM - 01:00 PM",
                    "activity": f"Experience morning rituals, folk artisan workshops, and souvenir shopping at festival grounds."
                },
                {
                    "time": "01:30 PM - 03:00 PM",
                    "activity": f"Lunch at heritage restaurant in {dest_city}."
                },
                {
                    "time": "03:30 PM - 06:30 PM",
                    "activity": f"Final view of {fest_name} procession / sports arena."
                },
                {
                    "time": "07:00 PM Onwards",
                    "activity": f"Pack up, checkout, and begin return travel back to {origin}."
                }
            ]
        }

        return {
            "origin": origin,
            "destination": dest_city,
            "festival_name": fest_name,
            "travel_date": date,
            "distance_km": distance_km,
            "mode_comparisons": mode_comparisons,
            "itinerary": {
                "day1": itinerary_day1,
                "day2": itinerary_day2
            }
        }

    def get_hotels_by_location(self, location: str) -> Dict[str, Any]:
        """Fetch hotels for a specified location (district, city, or festival)."""
        loc_clean = location.lower().strip()

        # Database lookup if available
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.hotel_name as name, h.distance_km, h.price_per_night, h.booking_url,
                       f.name as festival_name, f.district
                FROM hotels h
                JOIN festivals f ON h.festival_id = f.id
                WHERE LOWER(f.district) LIKE %s OR LOWER(f.city) LIKE %s OR LOWER(f.name) LIKE %s
            """, (f"%{loc_clean}%", f"%{loc_clean}%", f"%{loc_clean}%"))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            if rows:
                hotels = []
                for r in rows:
                    hotels.append({
                        "name": r["name"],
                        "distance_km": float(r["distance_km"]) if r["distance_km"] else 2.5,
                        "price_per_night": f"₹{r['price_per_night']}",
                        "rating": "4.6/5 ⭐",
                        "amenities": ["Free Wi-Fi", "AC", "Breakfast Included", "Parking"],
                        "booking_url": r["booking_url"] or f"https://booking.com/search?ss={r['name']}"
                    })
                return {
                    "location": location,
                    "count": len(hotels),
                    "hotels": hotels
                }
        except Exception:
            pass

        # Dynamic Mock Hotels matching location
        mock_hotels = [
            {
                "name": f"Royal Heritage Grand - {location.capitalize()}",
                "distance_km": 1.2,
                "price_per_night": "₹3,800",
                "rating": "4.8/5 ⭐",
                "amenities": ["Free Wi-Fi", "Palace View", "Pool", "Buffet Breakfast"],
                "booking_url": f"https://www.booking.com/search?ss=Royal+Heritage+{location}"
            },
            {
                "name": f"KSTDC Mayura Residency ({location.capitalize()})",
                "distance_km": 2.5,
                "price_per_night": "₹2,200",
                "rating": "4.4/5 ⭐",
                "amenities": ["Govt Approved", "Free Wi-Fi", "AC", "Restaurant"],
                "booking_url": f"https://www.kstdc.co/hotels/?location={location}"
            },
            {
                "name": f"Sanskriti Boutique Stay - {location.capitalize()}",
                "distance_km": 0.8,
                "price_per_night": "₹4,500",
                "rating": "4.9/5 ⭐",
                "amenities": ["Walk to Festival Grounds", "Authentic Food", "Spa"],
                "booking_url": f"https://www.agoda.com/search?city={location}"
            }
        ]

        return {
            "location": location,
            "count": len(mock_hotels),
            "hotels": mock_hotels
        }


# Global travel engine instance
travel_engine = TravelEngine()
