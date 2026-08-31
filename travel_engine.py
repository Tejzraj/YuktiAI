"""
YuktiAI - Travel Planner & Hotel Engine
Member 3: Simran
"""

import os
import json
import logging
import math
from typing import Dict, Any, List, Union, Optional
from datetime import datetime
import requests
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Prototype Estimation Assumptions ---
EST_BUS_RATE_PER_KM = 2.5
EST_TRAIN_RATE_PER_KM = 1.8
EST_CAB_RATE_PER_KM = 14.0
# ----------------------------------------

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

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "yuktiai"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password123"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

ROUTING_BASE_URL = os.getenv("ROUTING_BASE_URL", "http://router.project-osrm.org")


def load_festivals() -> List[Dict[str, Any]]:
    """Load festivals from PostgreSQL database or JSON dataset fallback."""
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(**DB_CONFIG, connect_timeout=1, cursor_factory=RealDictCursor)
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

    def _calculate_route(self, origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float) -> Dict[str, Any]:
        try:
            # OSRM expects lon,lat format
            url = f"{ROUTING_BASE_URL}/route/v1/driving/{origin_lon},{origin_lat};{dest_lon},{dest_lat}?overview=full&geometries=geojson"
            response = requests.get(url, timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == "Ok" and len(data.get("routes", [])) > 0:
                    route = data["routes"][0]
                    return {
                        "distance_km": round(route["distance"] / 1000.0, 1),
                        "duration_minutes": round(route["duration"] / 60.0),
                        "route_available": True,
                        "route_geometry": route.get("geometry")
                    }
        except Exception:
            pass
        
        return {
            "distance_km": 0,
            "duration_minutes": 0,
            "route_available": False,
            "route_geometry": None
        }

    def _calculate_transport_options(self, distance_km: float, duration_minutes: int, travellers: int) -> List[Dict[str, Any]]:
        if distance_km <= 0:
            return []

        options = []

        # 1. Bus Option
        bus_duration = int(duration_minutes * 1.2)  # Slower than direct road route
        bus_cost_pp = int(distance_km * EST_BUS_RATE_PER_KM)
        options.append({
            "mode": "Bus",
            "icon": "fa-bus",
            "estimated_time_minutes": bus_duration,
            "estimated_cost_per_person": bus_cost_pp,
            "estimated_total_cost": bus_cost_pp * travellers,
            "description": "State transport / private sleepers",
            "is_recommended": False,
            "recommendation_reason": ""
        })

        # 2. Train Option (Only if > 100km for MVP logic)
        if distance_km > 100:
            train_duration = int(duration_minutes * 0.9)  # Generally faster
            train_cost_pp = int(distance_km * EST_TRAIN_RATE_PER_KM)
            options.append({
                "mode": "Train",
                "icon": "fa-train",
                "estimated_time_minutes": train_duration,
                "estimated_cost_per_person": train_cost_pp,
                "estimated_total_cost": train_cost_pp * travellers,
                "description": "Express or Shatabdi",
                "is_recommended": False,
                "recommendation_reason": ""
            })

        # 3. Cab Option
        cabs_needed = math.ceil(travellers / 4.0)
        cab_total = int(distance_km * EST_CAB_RATE_PER_KM * cabs_needed)
        options.append({
            "mode": "Car / Cab",
            "icon": "fa-car",
            "estimated_time_minutes": duration_minutes,
            "estimated_cost_per_person": 0,  # Not billed per person
            "estimated_total_cost": cab_total,
            "description": f"{cabs_needed} vehicle(s) required",
            "is_recommended": False,
            "recommendation_reason": ""
        })

        # Find recommended option (e.g., Best Value = Train if available, else Bus)
        cheapest_option = min(options, key=lambda x: x["estimated_total_cost"])
        cheapest_option["is_recommended"] = True
        cheapest_option["recommendation_reason"] = "Best Value"

        return options

    def generate_travel_plan(self, origin: str, festival_id: Union[str, int], start_date: str, end_date: str = "", travellers: int = 1) -> Dict[str, Any]:
        fest = self._find_festival(festival_id)
        fest_name = fest.get("name", "Festival") if fest else "Karnataka Festival"
        dest_district = fest.get("district", "Karnataka") if fest else "Karnataka"
        dest_city = fest.get("city", dest_district) if fest else dest_district
        timings = fest.get("timings", "All Day") if fest else "All Day"

        # Determine Origin Coordinates
        orig_key = origin.lower().strip()
        origin_coords = HUB_COORDINATES.get(orig_key)
        
        # Determine Destination Coordinates
        dest_lat = fest.get("lat") if fest else None
        dest_lon = fest.get("lng") if fest else None

        route_info = {
            "distance_km": 0,
            "duration_minutes": 0,
            "route_available": False,
            "route_geometry": None
        }

        if origin_coords and dest_lat is not None and dest_lon is not None:
            route_info = self._calculate_route(origin_coords[0], origin_coords[1], float(dest_lat), float(dest_lon))

        distance_km = route_info["distance_km"]
        route_available = route_info["route_available"]
        
        transport_options = []
        if route_available:
            transport_options = self._calculate_transport_options(distance_km, route_info["duration_minutes"], travellers)

        return {
            "origin": origin,
            "destination": dest_city,
            "festival_name": fest_name,
            "travel_start_date": start_date,
            "travel_end_date": end_date,
            "travellers": travellers,
            "distance_km": distance_km,
            "route_available": route_available,
            "route_geometry": route_info["route_geometry"],
            "duration_minutes": route_info["duration_minutes"],
            "transport_options": transport_options
        }

    def generate_itinerary(self, origin: str, festival_id: Union[str, int], start_date_str: str, end_date_str: str, transport_mode: str, transport_duration_mins: int) -> List[Dict[str, Any]]:
        fest = self._find_festival(festival_id)
        fest_name = fest.get("name", "Festival") if fest else "Destination"
        
        # Parse Dates
        try:
            trip_start = datetime.strptime(start_date_str, "%Y-%m-%d")
            trip_end = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            return []

        total_days = (trip_end - trip_start).days + 1
        if total_days <= 0:
            return []
            
        fest_start_date = None
        fest_end_date = None
        if fest and "start_date" in fest and "end_date" in fest:
            try:
                fest_start_date = datetime.strptime(fest["start_date"], "%Y-%m-%d")
                fest_end_date = datetime.strptime(fest["end_date"], "%Y-%m-%d")
            except:
                pass
                
        itinerary = []
        for i in range(total_days):
            current_date = trip_start.fromtimestamp(trip_start.timestamp() + i * 86400)
            date_str = current_date.strftime("%d %b %Y")
            
            day_plan = {
                "day_number": i + 1,
                "date": date_str,
                "title": "",
                "activities": []
            }
            
            is_fest_day = False
            if fest_start_date and fest_end_date:
                if fest_start_date <= current_date <= fest_end_date:
                    is_fest_day = True
            
            activity_counter = 1
            def add_activity(time_str, activity_name, type_str, location_str):
                nonlocal activity_counter
                day_plan["activities"].append({
                    "id": f"day{i+1}_act{activity_counter}",
                    "time": time_str,
                    "activity": activity_name,
                    "type": type_str,
                    "location": location_str
                })
                activity_counter += 1

            # Day 1: Travel Day
            if i == 0:
                day_plan["title"] = f"{origin.capitalize()} to {fest_name}"
                hr = transport_duration_mins // 60
                mn = transport_duration_mins % 60
                dur_str = f"{hr} hr {mn} min" if hr > 0 else f"{mn} min"
                
                add_activity("Morning", f"Departure from {origin.capitalize()} ({transport_mode})", "Travel", f"Journey time: {dur_str}")
                add_activity("Afternoon", "Arrival & Hotel Check-in", "Rest", fest_name)
                add_activity("Evening", "Local Walk & Dinner", "Food", "Nearby Area")
                
            # Last Day: Return Journey (if total_days > 1)
            elif i == total_days - 1:
                day_plan["title"] = "Return Journey"
                add_activity("Morning", "Hotel Checkout", "Rest", fest_name)
                add_activity("Afternoon", f"Departure to {origin.capitalize()} ({transport_mode})", "Travel", "Return Journey")
                
            # Middle Days
            else:
                if is_fest_day:
                    day_plan["title"] = f"{fest_name} Celebrations"
                    
                    # Try to pull some actual attractions
                    attractions = fest.get("attractions", [])
                    food = fest.get("local_food", [])
                    
                    morn_act = attractions[0] if len(attractions) > 0 else "Explore Festival Grounds"
                    aft_act = food[0] if len(food) > 0 else "Local Cuisine Experience"
                    eve_act = attractions[1] if len(attractions) > 1 else "Evening Cultural Events"
                    
                    add_activity("10:00 AM", morn_act, "Festival", fest_name)
                    add_activity("01:00 PM", f"Lunch: {aft_act}", "Food", "Local Eatery")
                    add_activity("05:00 PM", eve_act, "Culture", fest_name)
                else:
                    day_plan["title"] = f"Explore {fest_name}"
                    add_activity("10:00 AM", "Visit Historic Landmarks", "Sightseeing", "City Center")
                    add_activity("02:00 PM", "Handicraft Market & Shopping", "Shopping", "Local Market")
                    add_activity("06:00 PM", "Enjoy Local Delicacies", "Food", "Popular Restaurant")
                    
            itinerary.append(day_plan)
            
        return itinerary

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
