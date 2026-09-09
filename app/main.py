from fastapi import FastAPI
from app.routers import sentiment

app = FastAPI()

app.include_router(sentiment.router)

@app.get("/")
def home():
    return "S'up fellas!"