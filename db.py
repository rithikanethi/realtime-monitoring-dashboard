import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

import urllib.parse as up
up.uses_netloc.append("postgres")

# Parse DB URI manually
db_url = os.getenv("DATABASE_URL")
parsed_url = up.urlparse(db_url)

conn = psycopg2.connect(
    dbname=parsed_url.path[1:],
    user=parsed_url.username,
    password=parsed_url.password,
    host=parsed_url.hostname,
    port=parsed_url.port
)

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
