from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging

app = FastAPI()
logger = logging.getLogger("uvicorn.access")

class review(BaseModel):
    name: str
    rating: int

reviews = {
    0: {"name": "Ivan", "rating": 73},
    1: {"name": "Anna", "rating": 69},
    2: {"name": "Dave", "rating": 87}
}
next_id = 3


@app.get("/reviews")
async def get_reviews(request: Request):
    logger.info(f"Request path: {request.url.path}, client: {request.client.host}")
    return list(reviews.values())

@app.get("/reviews/{id}")
async def get_review(id: int):
    if id not in reviews:
        raise HTTPException(status_code=404, detail="Not found")
    return reviews[id]

@app.post("/reviews", status_code=201)
async def add_review(review: review):
    global next_id
    reviews[next_id] = review.model_dump()
    next_id += 1
    return {"id": next_id - 1}

@app.put("/reviews/{id}")
async def update_review(id: int, review: review):
    if id not in reviews:
        raise HTTPException(status_code=404, detail="Not found")
    reviews[id] = review.model_dump()
    return {"id": id}

@app.delete("/reviews/{id}", status_code=204)
async def delete_review(id: int):
    if id not in reviews:
        raise HTTPException(status_code=404, detail="Not found")
    del reviews[id]
