from fastapi import FastAPI

app = FastAPI()

@app.get("/other")
async def get_other():
    return {"service": "other"}