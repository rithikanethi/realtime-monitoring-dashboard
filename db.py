
import psycopg2
from psycopg2.extras import RealDictCursor
import os

DB_URI = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DB_URI)
cursor = conn.cursor(cursor_factory=RealDictCursor)

def insert_metric(data):
    cursor.execute(
        "INSERT INTO metrics (service, cpu_usage, status) VALUES (%s, %s, %s);",
        (data["service"], data["cpu_usage"], data["status"])
    )
    conn.commit()

def get_recent_metrics():
    cursor.execute("SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 10;")
    return cursor.fetchall()
