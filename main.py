from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from db import insert_metric, get_recent_metrics

app = FastAPI()

# Enable CORS for frontend testing (optional, useful during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/metrics")
async def read_metrics():
    return await get_recent_metrics()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await insert_metric(data)

# Let Render auto-detect the FastAPI app
app = app
