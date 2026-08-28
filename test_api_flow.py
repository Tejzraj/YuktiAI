"""
YuktiAI / SanskritiPulse AI - End-to-End Integration Verification Suite
=====================================================================
Executes automated API testing across all multi-stakeholder endpoints:
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


def test_api_pipeline():
    print("================================================================")
    print("🚀 Running SanskritiPulse AI End-to-End Integration Tests")
    print("================================================================\n")

    passed_count = 0
    total_count = 0

    def assert_endpoint(name: str, method: str, path: str, payload: dict = None, expected_status: int = 200):
        nonlocal passed_count, total_count
        total_count += 1
        print(f"Testing [{method}] {path} ...", end=" ")

        if method == "GET":
            response = client.get(path)
        elif method == "POST":
            response = client.post(path, json=payload)
        else:
            raise ValueError("Unsupported method")

        if response.status_code == expected_status:
            passed_count += 1
            print(f"✅ PASSED (HTTP {response.status_code})")
            return response.json()
        else:
            print(f"❌ FAILED (HTTP {response.status_code}) - Details: {response.text}")
            return None

    # 1. Member 1 - Core Database & Festivals
    festivals_res = assert_endpoint("Get Festivals List", "GET", "/festivals")
    if festivals_res:
        print(f"   • Count: {festivals_res.get('count', 0)} festivals found")

    # 2. Member 2 - AI Recommendation & Translation
    rec_res = assert_endpoint("AI Recommend", "POST", "/recommend", payload={
        "interests": ["food", "folk", "culture", "heritage"]
    })
    if rec_res:
        recs = rec_res.get("recommendations", [])
        top_rec = recs[0] if recs else {}
        print(f"   • Top match: {top_rec.get('name')} (Score: {top_rec.get('score')}%)")

    trans_res = assert_endpoint("Translate to Kannada", "POST", "/translate", payload={
        "text": "Welcome to Mysuru Dasara festival",
        "target_lang": "kn"
    })
    if trans_res:
        print(f"   • Translated text: {trans_res.get('translated_text')}")

    # 3. Member 3 - Travel Planner & Hotels
    travel_res = assert_endpoint("Travel Plan Calculation", "POST", "/travel-plan", payload={
        "origin": "Bangalore",
        "festival_id": "mysuru-dasara",
        "date": "2026-10-15"
    })
    if travel_res:
        print(f"   • Modes: {len(travel_res.get('mode_comparisons', []))} transit options")

    hotel_res = assert_endpoint("Nearby Hotels Search", "GET", "/hotels/Mysuru")
    if hotel_res:
        print(f"   • Hotels found: {hotel_res.get('count', 0)}")

    # 4. Member 5 - Gov Analytics & Crowd Risk
    overview_res = assert_endpoint("Analytics Overview", "GET", "/analytics/overview")
    if overview_res:
        print(f"   • Total Visitors Expected: {overview_res.get('total_expected_visitors')} (High-Risk Events: {overview_res.get('high_risk_events_count')})")

    map_res = assert_endpoint("Analytics GeoJSON Map Data", "GET", "/analytics/map-data")
    if map_res:
        print(f"   • GeoJSON Markers: {len(map_res.get('features', []))} features")

    trends_res = assert_endpoint("Analytics Footfall Trends", "GET", "/analytics/trends")
    if trends_res:
        print(f"   • Category Distribution Items: {len(trends_res.get('category_distribution', []))}")

    # 5. Member 6 - Organizer Site Ops & Live Announcements
    ops_res = assert_endpoint("Organizer Overview", "GET", "/organizer/overview/mysuru-dasara")
    if ops_res:
        print(f"   • Real-Time Visitors: {ops_res.get('realtime_visitor_estimate', ops_res.get('current_visitors'))}")

    post_ann_res = assert_endpoint("Create Announcement", "POST", "/organizer/announcement", payload={
        "festival_id": "mysuru-dasara",
        "message": "Jamboo Savari procession starts at 4:00 PM today!"
    })
    if post_ann_res:
        print(f"   • Announcement Saved ID: {post_ann_res.get('data', {}).get('id')}")

    get_ann_res = assert_endpoint("Get Announcements for Tourist Dashboard", "GET", "/announcements/mysuru-dasara")
    if get_ann_res:
        print(f"   • Announcements Count: {get_ann_res.get('count', 0)}")

    print("\n================================================ me")
    print(f"📊 Summary: {passed_count}/{total_count} Endpoints Verified Successfully (HTTP 200 OK)")
    print("================================================================")

    if passed_count < total_count:
        sys.exit(1)


if __name__ == "__main__":
    test_api_pipeline()
