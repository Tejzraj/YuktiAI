"""
SanskritiPulse AI - Travel Planner & Hotel Engine (Haversine Distance Math)
Member 3: Simran
"""

import os
import json
import math
from pathlib import Path
from typing import List, Dict, Any, Union, Optional
from database import get_db_connection, DB_CONFIG

# Major Karnataka starting hubs coordinates (lat, lng)
KARNATAKA_HUBS = {
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
    "kalaburagi": (17.3297, 76.8343),
    "shivamogga": (13.9299, 75.5681)
}


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate Great-Circle Haversine distance between two GPS coordinates in kilometers.
    """
    R = 6371.0  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2.0)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    direct_distance = R * c
    # Multiply by road circuity factor (~1.25) to convert geodesic distance to actual road route distance
    road_distance = direct_distance * 1.25
    return round(road_distance, 1)


def load_festivals() -> List[Dict[str, Any]]:
    """Load festivals dataset from DB or JSON file fallback."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.id, f.festival_id, f.name, f.district, f.city, f.latitude, f.longitude,
                   f.timings, f.short_description, f.major_attractions, f.local_food,
                   c.name as category
            FROM festivals f
            LEFT JOIN festival_categories c ON f.category_id = c.id
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if rows:
            data = []
            for r in rows:
                item = dict(r)
                item["id"] = item.get("festival_id") or item.get("id")
                item["latitude"] = float(item["latitude"]) if item.get("latitude") else 12.9716
                item["longitude"] = float(item["longitude"]) if item.get("longitude") else 77.5946
                data.append(item)
            return data
    except Exception:
        pass

    candidates = [
        Path(__file__).parent.parent.parent / "database" / "mock_festivals.json",
        Path(__file__).parent.parent / "database" / "mock_festivals.json",
        Path.cwd() / "database" / "mock_festivals.json",
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
            "latitude": 12.3051,
            "longitude": 76.6551,
            "timings": "9:00 AM - 10:00 PM"
        },
        {
            "id": "hampi-utsav",
            "name": "Hampi Utsav",
            "district": "Vijayanagara",
            "city": "Hampi",
            "latitude": 15.3350,
            "longitude": 76.4600,
            "timings": "10:00 AM - 11:00 PM"
        }
    ]


class TravelEngine:
    def __init__(self):
        self.festivals = load_festivals()

    def _find_festival(self, fest_id_or_name: Union[str, int]) -> Optional[Dict[str, Any]]:
        target = str(fest_id_or_name).lower().strip()
        for f in self.festivals:
            f_id = str(f.get("id", "")).lower()
            f_name = str(f.get("name", "")).lower()
            if target == f_id or target in f_name or f_id in target:
                return f
        return self.festivals[0] if self.festivals else None

    def calculate_travel_plan(self, starting_city: str, destination_festival: str, start_date: str, end_date: str = None, number_of_people: int = 1) -> Dict[str, Any]:
        """Calculates transit options, Haversine road distances, costs, group budget, and 2-day itinerary."""
        fest = self._find_festival(destination_festival)
        fest_name = fest.get("name", "Karnataka Festival") if fest else "Karnataka Festival"
        dest_city = fest.get("city") or fest.get("district", "Karnataka") if fest else "Karnataka"
        timings = fest.get("timings", "All Day") if fest else "All Day"

        # Determine origin coordinates
        orig_key = starting_city.lower().strip()
        orig_coords = KARNATAKA_HUBS.get(orig_key, (12.9716, 77.5946))  # Default Bangalore

        # Destination coordinates
        dest_lat = float(fest.get("latitude") or fest.get("lat") or 12.3051) if fest else 12.3051
        dest_lng = float(fest.get("longitude") or fest.get("lng") or 76.6551) if fest else 76.6551

        # Calculate exact Haversine distance
        distance_km = haversine_distance(orig_coords[0], orig_coords[1], dest_lat, dest_lng)
        if distance_km < 10.0:
            distance_km = 145.0  # Sanity fallback if same city selected

        # Calculate modes (per person & total group)
        bus_hrs = max(1.5, round(distance_km / 48.0, 1))
        bus_pp = int(distance_km * 2.2)
        bus_total = bus_pp * number_of_people

        train_hrs = max(1.2, round(distance_km / 58.0, 1))
        train_pp = int(distance_km * 1.5)
        train_total = train_pp * number_of_people

        car_hrs = max(1.0, round(distance_km / 72.0, 1))
        car_total = int(distance_km * 7.5)
        car_pp = int(car_total / max(1, number_of_people))

        mode_comparisons = [
            {
                "mode": "KSRTC Airavat Bus",
                "duration": f"{bus_hrs} hrs",
                "estimated_cost_per_person": f"₹{bus_pp}",
                "total_group_cost": f"₹{bus_total}",
                "distance_km": distance_km,
                "recommended_for": "Frequent Direct Routes"
            },
            {
                "mode": "Express Train",
                "duration": f"{train_hrs} hrs",
                "estimated_cost_per_person": f"₹{train_pp}",
                "total_group_cost": f"₹{train_total}",
                "distance_km": distance_km,
                "recommended_for": "Scenic & Comfortable Journey"
            },
            {
                "mode": "Private Car / SUV Taxi",
                "duration": f"{car_hrs} hrs",
                "estimated_cost_per_person": f"₹{car_pp}",
                "total_group_cost": f"₹{car_total}",
                "distance_km": distance_km,
                "recommended_for": "Families & Flexible Schedule"
            }
        ]

        itinerary_day1 = {
            "day": 1,
            "title": f"Departure from {starting_city.capitalize()} & Festival Arrival",
            "schedule": [
                { "time": "07:00 AM - 11:30 AM", "activity": f"Travel from {starting_city.capitalize()} to {dest_city} ({distance_km} km)." },
                { "time": "12:00 PM - 01:30 PM", "activity": f"Check-in at hotel in {dest_city}, freshen up & enjoy authentic lunch." },
                { "time": "02:30 PM - 05:30 PM", "activity": f"Visit {fest_name} main venue & cultural exhibitions." },
                { "time": "06:00 PM - 09:30 PM", "activity": f"Witness evening illuminations & cultural shows ({timings})." }
            ]
        }

        itinerary_day2 = {
            "day": 2,
            "title": f"Heritage Discovery & Return to {starting_city.capitalize()}",
            "schedule": [
                { "time": "08:00 AM - 10:00 AM", "activity": "Breakfast with local food specialties & morning temple walk." },
                { "time": "10:30 AM - 01:00 PM", "activity": f"Explore handicraft stalls and artisan markets at {fest_name}." },
                { "time": "01:30 PM - 03:00 PM", "activity": f"Traditional lunch in {dest_city}." },
                { "time": "04:00 PM Onwards", "activity": f"Checkout and return trip back to {starting_city.capitalize()}." }
            ]
        }

        return {
            "starting_city": starting_city,
            "destination_festival": fest_name,
            "travel_date": start_date,
            "number_of_people": number_of_people,
            "haversine_distance_km": distance_km,
            "mode_comparisons": mode_comparisons,
            "itinerary": {
                "day1": itinerary_day1,
                "day2": itinerary_day2
            }
        }

    def get_hotels_by_location(self, location: str) -> Dict[str, Any]:
        """Fetch hotels for a specified location."""
        loc_clean = location.lower().strip()

        mock_hotels = [
            {
                "name": f"Royal Heritage Grand ({location.capitalize()})",
                "distance_km": 1.2,
                "price_per_night": "₹3,800",
                "rating": "4.8/5 ⭐",
                "amenities": ["Free Wi-Fi", "Palace View", "Pool", "Buffet Breakfast"],
                "booking_url": f"https://www.booking.com/search?ss={location}"
            },
            {
                "name": f"KSTDC Mayura Hotel ({location.capitalize()})",
                "distance_km": 2.1,
                "price_per_night": "₹2,200",
                "rating": "4.4/5 ⭐",
                "amenities": ["Govt Approved", "AC", "Restaurant"],
                "booking_url": f"https://www.kstdc.co/hotels/?location={location}"
            },
            {
                "name": f"Sanskriti Boutique Stay ({location.capitalize()})",
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


# Global instance
travel_engine = TravelEngine()
