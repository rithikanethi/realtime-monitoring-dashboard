import logging
from fastapi import FastAPI
from db import insert_metric, get_recent_metrics, database

app = FastAPI()

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

@app.get("/")
def root():
    return {"message": "API is live!"}

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/metrics")
async def read_metrics():
    try:
        data = await get_recent_metrics()
        return data
    except Exception as e:
        logging.exception("Error fetching metrics:")
        return {"error": str(e)}