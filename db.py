from databases import Database
import os

# Load the DATABASE_URL from environment variable
DB_URI = os.getenv("DATABASE_URL")
database = Database(DB_URI)

# Connect and disconnect functions
async def connect_db():
    await database.connect()

async def disconnect_db():
    await database.disconnect()

# Insert a new metric into the metrics table
async def insert_metric(data):
    query = "INSERT INTO metrics (service, cpu_usage, status) VALUES (:service, :cpu_usage, :status)"
    await database.execute(query=query, values=data)

# Retrieve the 10 most recent metrics
async def get_recent_metrics():
    query = "SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 10"
    return await database.fetch_all(query=query)