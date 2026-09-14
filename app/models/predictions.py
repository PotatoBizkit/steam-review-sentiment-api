from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime, timezone
from app.database import Base

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    review_text = Column(String, nullable=False)
    recommendation = Column(Boolean, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))