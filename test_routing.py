import json
from travel_engine import travel_engine

def test_routing():
    print("Testing Valid Route (Bangalore to Mysuru Dasara)...")
    plan1 = travel_engine.generate_travel_plan("bangalore", "mysuru-dasara", "2026-10-15", "2026-10-17", 2)
    assert plan1["route_available"] == True
    assert plan1["distance_km"] > 0
    print(f"Distance: {plan1['distance_km']} km, Duration: {plan1['duration_minutes']} min, Travellers: {plan1['travellers']}")
    
    print("\nTesting Unknown Origin (Nowhere)...")
    plan2 = travel_engine.generate_travel_plan("nowhere", "mysuru-dasara", "2026-10-15", "2026-10-17", 2)
    assert plan2["route_available"] == False
    assert plan2["distance_km"] == 0
    print("Route Unavailable successfully verified.")
    
    print("\nTesting Invalid Festival (Unknown)...")
    plan3 = travel_engine.generate_travel_plan("bangalore", "invalid-fest-id", "2026-10-15", "2026-10-17", 2)
    # Will fallback to first festival in load_festivals(), which is Mysuru Dasara
    print(f"Fallback Festival Used: {plan3['festival_name']}")
    assert plan3["route_available"] == True
    
    print("\nAll routing tests completed successfully!")

if __name__ == "__main__":
    test_routing()
