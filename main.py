
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from db import insert_metric, get_recent_metrics
import uvicorn

app = FastAPI()

# Enable CORS for frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/metrics")
async def read_metrics():
    return get_recent_metrics()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        insert_metric(data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
