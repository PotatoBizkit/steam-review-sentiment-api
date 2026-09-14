from fastapi import FastAPI
from app.routers import sentiment
from app.database import Base, engine
from app.models.predictions import Prediction

app = FastAPI()

app.include_router(sentiment.router)

@app.get("/")
def home():
    return "S'up fellas!"

Base.metadata.create_all(bind=engine)