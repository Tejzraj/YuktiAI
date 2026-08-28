"""
SanskritiPulse AI - End-to-End Test Suite for Refactored Modular Application
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add backend/app to sys.path
sys.path.insert(0, str(Path(__file__).parent / "backend" / "app"))

from main import app

client = TestClient(app)


def test_refactored_architecture():
    print("================================================================")
    print("🚀 Running SanskritiPulse AI Modular Refactor Test Suite")
    print("================================================ failure\n")

    passed_count = 0
    total_count = 0

    def assert_route(name: str, method: str, path: str, payload: dict = None, expected_status: int = 200):
        nonlocal passed_count, total_count
        total_count += 1
        print(f"Testing [{method}] {path} ({name}) ...", end=" ")

        if method == "GET":
            response = client.get(path)
        elif method == "POST":
            response = client.post(path, json=payload)
        else:
            raise ValueError("Unsupported method")

        if response.status_code == expected_status:
            passed_count += 1
            print(f"✅ PASSED (HTTP {response.status_code})")
            return response
        else:
            print(f"❌ FAILED (HTTP {response.status_code}) - Details: {response.text}")
            return None

    # 1. UI Root Route
    assert_route("Single-Page Application UI", "GET", "/")

    # 2. Authentication
    assert_route("User Registration", "POST", "/auth/register", payload={
        "username": "test_organizer",
        "password": "password123",
        "role": "organizer"
    })

    assert_route("User Login", "POST", "/auth/login", payload={
        "username": "test_organizer",
        "password": "password123"
    })

    # 3. Master Festivals
    assert_route("Get Festivals", "GET", "/festivals")

    # 4. AI Recommendation & Translation
    assert_route("AI Recommendation", "POST", "/recommend", payload={
        "interests": ["food", "folk", "culture"]
    })

    assert_route("Multilingual Translation", "POST", "/translate", payload={
        "text": "Welcome to Mysuru Dasara festival",
        "target_lang": "kn"
    })

    # 5. Travel Planner & Tourist Guide
    travel_res = assert_route("Haversine Travel Planner", "POST", "/travel-plan", payload={
        "starting_city": "Bangalore",
        "destination_festival": "mysuru-dasara",
        "start_date": "2026-10-15",
        "number_of_people": 2
    })
    if travel_res:
        plan = travel_res.json()
        print(f"   • Haversine Distance: {plan.get('haversine_distance_km')} km")

    assert_route("Nearby Hotels Search", "GET", "/hotels/mysuru-dasara")

    guide_res = assert_route("AI Tourist Guide Modal", "GET", "/tourist-guide/mysuru-dasara")
    if guide_res:
        print(f"   • Guide Title: {guide_res.json().get('name')}")

    # 6. Gov Analytics
    assert_route("Analytics Overview", "GET", "/analytics/overview")
    assert_route("GIS Map GeoJSON", "GET", "/analytics/map-data")
    assert_route("Analytics Trends", "GET", "/analytics/trends")

    # 7. Organizer Site Ops & Live Publishing
    assert_route("Site Ops Overview", "GET", "/organizer/overview/mysuru-dasara")
    assert_route("Publish Announcement", "POST", "/organizer/announcement", payload={
        "festival_id": "mysuru-dasara",
        "message": "Illuminations start at 7:00 PM today."
    })
    assert_route("Fetch Announcements", "GET", "/announcements/mysuru-dasara")

    pub_res = assert_route("Publish New Festival Event", "POST", "/organizer/publish-festival", payload={
        "name": "Gavisiddheshwara Jatre",
        "district": "Koppal",
        "category": "Spiritual & Folk",
        "expected_footfall": 500000
    })
    if pub_res:
        print(f"   • Published Event: {pub_res.json().get('festival', {}).get('name')}")

    print("\n================================================================")
    print(f"📊 Summary: {passed_count}/{total_count} Refactored Routes Verified (HTTP 200 OK)")
    print("================================================================")

    if passed_count < total_count:
        sys.exit(1)


if __name__ == "__main__":
    test_refactored_architecture()
