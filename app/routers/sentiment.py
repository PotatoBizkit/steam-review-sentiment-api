import joblib
from fastapi import APIRouter
from app.schemas.sentiment import SentimentOutput, ReviewInput

router = APIRouter(prefix="/sentiment", tags=["Sentiment"])
model = joblib.load("app/models/sentiment_model.pkl")
vectorizer = joblib.load("app/models/tfidf_vectorizer.pkl")

@router.post("/predict", response_model=SentimentOutput)
def predict_sentiment(data: ReviewInput)
    txt_tfidf = vectorizer.transform([data.review_text])
    pred = model.predict(txt_tfidf)[0]
    prob = model.predict_proba(txt_tfidf)[0]
    confidence = float(max(probability))

    return SentimentOutput(
        review_text=payload.review_text,
        recommendation=bool(prediction),
        confidence=confidence
    )