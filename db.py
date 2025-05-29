import os
import psycopg2
from psycopg2.extras import RealDictCursor
import socket

# Force IPv4 resolution to avoid Render IPv6 issues
def force_ipv4():
    original_getaddrinfo = socket.getaddrinfo

    def getaddrinfo_ipv4(*args, **kwargs):
        return [info for info in original_getaddrinfo(*args, **kwargs) if info[0] == socket.AF_INET]

    socket.getaddrinfo = getaddrinfo_ipv4

force_ipv4()

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
