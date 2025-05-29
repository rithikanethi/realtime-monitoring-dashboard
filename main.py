
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from db import insert_metric, get_recent_metrics, database
import uvicorn

app = FastAPI()

# Enable CORS for frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Connect to database when app starts
@app.on_event("startup")
async def startup():
    await database.connect()

# Disconnect when app shuts down
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/metrics")
async def read_metrics():
    return await get_recent_metrics()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await insert_metric(data)
