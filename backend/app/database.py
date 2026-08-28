"""
SanskritiPulse AI - Database Pool & Connection Module
"""
import os
from typing import Optional, Any

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
