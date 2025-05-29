from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import os
from db import insert_metric, get_recent_metrics, database

app = FastAPI()

# Enable CORS for frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def root():
    return {"message": "Service is running!"}

@app.get("/metrics")
async def read_metrics():
    try:
        return await get_recent_metrics()
    except Exception as e:
        return {"error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await insert_metric(data)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # default to 10000 if not set
    uvicorn.run(app, host="0.0.0.0", port=port)