import os
import databases
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
database = databases.Database(DATABASE_URL)

async def insert_metric(data):
    query = """
        INSERT INTO metrics (service, cpu_usage, status)
        VALUES (:service, :cpu_usage, :status)
    """
    await database.execute(query=query, values=data)

async def get_recent_metrics():
    query = "SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 10"
    return await database.fetch_all(query=query)