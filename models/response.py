from datetime import datetime

from pydantic import BaseModel


class PredictionOut(BaseModel):
    prediction: str
    probability: str
    timestamp: datetime
    process_time: str
