
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Shipment(BaseModel):
    name: str
    tracking: str

shipments = [
    {"name": "Ivan", "tracking": "83dcefb7"},
    {"name": "Anna", "tracking": "1ad5be0d"},
    {"name": "Dave", "tracking": "6dd28e9b"}
]

shipments = {}
next_id = 0

@app.get("/shipments")
async def get_shipments():
    return shipments

@app.get("/shipments/{id}")
async def get_shipment(id: int):
    if id not in shipments:
        raise HTTPException(status_code=404, detail="Not found")
    return shipments[id]

@app.post("/shipments", status_code=201)
async def add_shipment(shipment: Shipment):
    global next_id
    shipments[next_id] = shipment.model_dump()
    next_id += 1
    return {"id": next_id - 1}

@app.put("/shipments/{id}")
async def update_shipment(id: int, shipment: Shipment):
    if id not in shipments:
        raise HTTPException(status_code=404, detail="Not found")
    shipments[id] = shipment.model_dump()
    return {"id": id}

@app.delete("/shipments/{id}", status_code=204)
async def delete_shipment(id: int):
    if id not in shipments:
        raise HTTPException(status_code=404, detail="Not found")
    del shipments[id]

