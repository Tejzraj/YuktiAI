import psycopg2
import pandas as pd

DB_CONFIG = {
    "dbname": "sanskritipulse",
    "user": "postgres",
    "password": "password123",
    "host": "localhost",
    "port": "5432"
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
    print("✅ Created festivals_backup.csv and categories_backup.csv")

if __name__ == "__main__":
    export_backups()