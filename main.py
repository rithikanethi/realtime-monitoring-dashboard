from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from db import insert_metric, get_recent_metrics, database
import uvicorn
import os

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
async def root():
    return {"message": "Realtime Monitoring Dashboard API is running"}

@app.get("/metrics")
async def read_metrics():
    try:
        return await get_recent_metrics()
    except Exception as e:
        return {"error": str(e)}

@app.post("/metrics")
async def post_metrics(request: Request):
    try:
        data = await request.json()
        await insert_metric(data)
        return {"message": "Metric added"}
    except Exception as e:
        return {"error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            await insert_metric(data)
        except Exception as e:
            await websocket.send_json({"error": str(e)})

# ✅ Correct port binding for Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)