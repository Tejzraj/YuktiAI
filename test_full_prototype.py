"""
YuktiAI / SanskritiPulse AI - Full Prototype Integration Test Suite
===================================================================
Tests all backend API endpoints and static UI root route:
- GET  /
- GET  /festivals
- POST /recommend
- POST /translate
- POST /travel-plan
- GET  /hotels/{location}
- GET  /analytics/overview
- GET  /analytics/map-data
- GET  /analytics/trends
- GET  /organizer/overview/{festival_id}
- POST /organizer/announcement
- GET  /announcements/{festival_id}
"""

import sys
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_full_prototype_suite():
    print("================================================================")
    print("🚀 Running SanskritiPulse AI Full Prototype Test Suite")
    print("================================================================\n")

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

    # 1. Static UI Route
    ui_res = assert_route("Single-Page Web UI", "GET", "/")
    if ui_res:
        assert "<html" in ui_res.text.lower()
        print("   • HTML5 UI file served successfully")

    # 2. Member 1 - Core Dataset
    festivals_res = assert_route("Get Festivals", "GET", "/festivals")
    if festivals_res:
        print(f"   • Festivals returned: {festivals_res.json().get('count', 0)}")

    # 3. Member 2 - AI Recommendation & Multilingual
    rec_res = assert_route("AI Recommendation", "POST", "/recommend", payload={
        "interests": ["food", "folk", "culture"]
    })
    if rec_res:
        top = rec_res.json().get("recommendations", [])[0]
        print(f"   • Top match: {top.get('name')} (Score: {top.get('score')}%)")

    trans_res = assert_route("Multilingual Translation", "POST", "/translate", payload={
        "text": "Welcome to Mysuru Dasara festival",
        "target_lang": "kn"
    })
    if trans_res:
        print(f"   • Translation: {trans_res.json().get('translated_text')}")

    # 4. Member 3 - Travel Planner & Hotels
    travel_res = assert_route("Travel Route & Itinerary", "POST", "/travel-plan", payload={
        "origin": "Bangalore",
        "festival_id": "mysuru-dasara",
        "date": "2026-10-15"
    })
    if travel_res:
        print(f"   • Transit modes returned: {len(travel_res.json().get('mode_comparisons', []))}")

    hotel_res = assert_route("Nearby Hotels Search", "GET", "/hotels/mysuru-dasara")
    if hotel_res:
        print(f"   • Hotels returned: {hotel_res.json().get('count', 0)}")

    # 5. Member 5 - Gov Analytics & Crowd Risk
    overview_res = assert_route("Analytics Overview", "GET", "/analytics/overview")
    if overview_res:
        print(f"   • Total Visitors: {overview_res.json().get('total_expected_visitors')}")

    map_res = assert_route("GIS Map GeoJSON", "GET", "/analytics/map-data")
    if map_res:
        print(f"   • Map Markers: {len(map_res.json().get('features', []))}")

    trends_res = assert_route("Analytics Trends", "GET", "/analytics/trends")
    if trends_res:
        print(f"   • District Distribution Items: {len(trends_res.json().get('district_distribution', []))}")

    # 6. Member 6 - Organizer Site Ops & Broadcast Announcements
    ops_res = assert_route("Site Ops Overview", "GET", "/organizer/overview/mysuru-dasara")
    if ops_res:
        print(f"   • Live Spectators: {ops_res.json().get('realtime_visitor_estimate', ops_res.json().get('current_visitors'))}")

    post_ann_res = assert_route("Publish Announcement", "POST", "/organizer/announcement", payload={
        "festival_id": "mysuru-dasara",
        "message": "Live updates: Gate 2 illuminations starting at 7 PM."
    })
    if post_ann_res:
        print(f"   • Announcement ID: {post_ann_res.json().get('data', {}).get('id')}")

    get_ann_res = assert_route("Fetch Announcements", "GET", "/announcements/mysuru-dasara")
    if get_ann_res:
        print(f"   • Announcements Count: {get_ann_res.json().get('count', 0)}")

    print("\n================================================================")
    print(f"📊 Summary: {passed_count}/{total_count} Prototype Routes Verified (HTTP 200 OK)")
    print("================================================================")

    if passed_count < total_count:
        sys.exit(1)


if __name__ == "__main__":
    test_full_prototype_suite()
