from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str

users = [
    {"name": "Ivan", "email": "123@test.com"},
    {"name": "Anna", "email": "anna@test.com"},
    {"name": "Dave", "email": "crazydave@test.com"}
]

@app.get("/users")
async def get_users():
    return users

@app.get("/users/{id}")
async def get_user(id: int):
    if id < 0 or id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    return users[id]

@app.post("/users", status_code=201)
async def add_user(user: User):
    users.append(user.model_dump())
    return {"id": len(users) - 1}
