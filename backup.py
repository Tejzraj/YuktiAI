import os
import psycopg2
import pandas as pd

# Database Connection Settings matching docker-compose.yml
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "yuktiai"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password123"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

def export_backups():
    conn = psycopg2.connect(**DB_CONFIG)
    
    # Export Festivals table to CSV
    df_festivals = pd.read_sql_query("SELECT * FROM festivals;", conn)
    df_festivals.to_csv("festivals_backup.csv", index=False)
    
    # Export Categories to CSV
    df_categories = pd.read_sql_query("SELECT * FROM festival_categories;", conn)
    df_categories.to_csv("categories_backup.csv", index=False)
    
    conn.close()
    print("✅ Created festivals_backup.csv and categories_backup.csv for YuktiAi database")

if __name__ == "__main__":
    export_backups()