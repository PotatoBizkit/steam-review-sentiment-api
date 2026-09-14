import joblib
from fastapi import APIRouter, Depends
from app.schemas.sentiment import SentimentOutput, ReviewInput
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.predictions import Prediction

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
router = APIRouter(prefix="/sentiment", tags=["Sentiment"])
model = joblib.load("app/models/sentiment_model.pkl")
vectorizer = joblib.load("app/models/tfidf_vectorizer.pkl")

@router.post("/predict", response_model=SentimentOutput)
def predict_sentiment(data: ReviewInput, db: Session = Depends(get_db)):
    txt_tfidf = vectorizer.transform([data.review_text])
    pred = model.predict(txt_tfidf)[0]
    prob = model.predict_proba(txt_tfidf)[0]
    confidence = float(max(prob))
    db_entry = Prediction(review_text=data.review_text, recommendation=bool(pred), confidence=confidence)
    db.add(db_entry)
    db.commit()
    return SentimentOutput(
        review_text = data.review_text,
        recommendation = bool(pred),
        confidence = confidence
    )