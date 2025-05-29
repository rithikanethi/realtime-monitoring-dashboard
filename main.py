from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from db import insert_metric, get_recent_metrics

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
    return await get_recent_metrics()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await insert_metric(data)

# Explicitly bind app to a port for Render to detect
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=False)
