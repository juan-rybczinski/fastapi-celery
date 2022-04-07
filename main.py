from datetime import datetime

from fastapi import FastAPI, Depends

from models.request import PathIn
from models.response import PredictionOut
from utils.ml import engine, init_model
from prediction.tasks import by_path

app = FastAPI()

init_model()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/path", response_model=PredictionOut)
async def predict_by_path(path_in: PathIn = Depends(PathIn.as_form)):
    start = datetime.now()
    result = engine.run_by_path(path_in.path)
    timestamp = get_timestamp(start, datetime.now())
    return PredictionOut(**result, **timestamp)


@app.post("/path_q", response_model=PredictionOut)
async def predict_by_path_q(path_in: PathIn = Depends(PathIn.as_form)):
    start = datetime.now()
    celery_result = by_path.delay(path_in.path)
    result = celery_result.get(timeout=5)
    timestamp = get_timestamp(start, datetime.now())
    return PredictionOut(**result, **timestamp)


def get_timestamp(start: datetime, end: datetime):
    return {"timestamp": end.strftime("%Y-%m-%d %H:%M:%S"),
            "process_time": str(int((end - start).total_seconds() * 1000))}