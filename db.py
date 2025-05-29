from databases import Database
import os
# Load the database URL from the environment (.env or Render settings)
DB_URI = os.getenv("DATABASE_URL")

# Create a database instance using asyncpg (handled internally by databases)
database = Database(DB_URI)

# Insert a new metric into the 'metrics' table
async def insert_metric(data):
    query = """
        INSERT INTO metrics (service, cpu_usage, status)
        VALUES (:service, :cpu_usage, :status)
    """
    await database.execute(query=query, values=data)

# Fetch the 10 most recent metrics, ordered by timestamp
async def get_recent_metrics():
    query = """
        SELECT * FROM metrics
        ORDER BY timestamp DESC
        LIMIT 10
    """
    return await database.fetch_all(query=query)