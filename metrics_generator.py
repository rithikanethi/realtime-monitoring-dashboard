
import time
import random
import json
import asyncio
import websockets

async def send_metrics():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            data = {
                "service": "data-cleaner",
                "cpu_usage": round(random.uniform(10.0, 90.0), 2),
                "status": "running" if random.random() > 0.1 else "failed"
            }
            await websocket.send(json.dumps(data))
            await asyncio.sleep(2)

asyncio.run(send_metrics())
