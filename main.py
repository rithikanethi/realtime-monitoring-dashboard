from fastapi import FastAPI, WebSocket
from db import connect_db, disconnect_db, insert_metric, get_recent_metrics

app = FastAPI()

# Root route just for testing if the server is up
@app.get("/")
async def root():
    return {"message": "Real-time monitoring dashboard is running."}

# Connect to DB when server starts
@app.on_event("startup")
async def startup():
    await connect_db()

# Disconnect DB when server shuts down
@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

# Endpoint to fetch recent metrics
@app.get("/metrics")
async def read_metrics():
    return await get_recent_metrics()

# WebSocket to receive live metrics
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await insert_metric(data)