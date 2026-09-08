from pydantic import BaseModel

class ReviewInput(BaseModel):
    review_text: str

class SentimentOutput(BaseModel):
    review_text: str
    recommendation: bool
    confidence: float