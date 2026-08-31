"""
SanskritiPulse AI - Database Pool & Connection Module
"""
import os
import json
from pathlib import Path
from typing import Optional, Any, List, Dict

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "sanskritipulse"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password123"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "connect_timeout": 1
}


def get_db_connection():
    import psycopg2
    from psycopg2.extras import RealDictCursor
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


def save_festivals_to_json(festivals: List[Dict[str, Any]]) -> bool:
    """Save in-memory festivals back to mock_festivals.json database file."""
    candidates = [
        Path(__file__).parent.parent.parent / "database" / "mock_festivals.json",
        Path(__file__).parent.parent / "database" / "mock_festivals.json",
        Path.cwd() / "database" / "mock_festivals.json",
        Path.cwd() / "festivals_karnataka.json",
    ]
    for p in candidates:
        if p.parent.exists():
            try:
                # We can save it with formatting
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(festivals, f, indent=2, ensure_ascii=False)
                return True
            except Exception as e:
                print(f"⚠️ Failed to write to {p}: {e}")
    return False
