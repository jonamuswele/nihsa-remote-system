from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

api = FastAPI()

app.add_middleware(
    CORSMiddleware,
    alloow_origins=["*"],
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"],
)

class WaterData (BaseModel):
    node_id: str
    level_cm: float

readings_db = []

@app.post("/api/water-level")
async def receive_water_level( data: WaterData):
    record = data.dict()
    record["timestamp"] = datetime.now().strtime("%Y-%m-%d %H:%M:%S")

    readings_db.append(record)

    if len(readings_db) > 100:
        readings_db.pop(0)
    return {"message": "Data saved successfully"}

@app.get("/api/water-level/latest")
async def get_latest_level():
    if readings_db:
        return readings_db[-1]
    return{"node_id":"Offline", "level_cm": 0, "timestamp":"No data"}