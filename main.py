from datetime import datetime
import io
import base64

from fastapi import FastAPI, Depends

from models.request import PathIn, ImageIn
from models.response import PredictionOut
from utils.ml import engine, init_model
from prediction.tasks import by_path, by_file

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


@app.post("/file", response_model=PredictionOut)
async def predict_by_path(image_in: ImageIn = Depends(ImageIn.as_form)):
    start = datetime.now()

    img = await image_in.img.read()
    result = engine.run(io.BytesIO(img))

    timestamp = get_timestamp(start, datetime.now())

    return PredictionOut(**result, **timestamp)


@app.post("/path_q", response_model=PredictionOut)
async def predict_by_path_q(path_in: PathIn = Depends(PathIn.as_form)):
    start = datetime.now()

    celery_result = by_path.delay(path_in.path)
    result = celery_result.get(timeout=5)

    timestamp = get_timestamp(start, datetime.now())

    return PredictionOut(**result, **timestamp)


@app.post("/file_q", response_model=PredictionOut)
async def predict_by_file_q(image_in: ImageIn = Depends(ImageIn.as_form)):
    start = datetime.now()

    img = await image_in.img.read()
    img = base64.b64encode(img)
    celery_result = by_file.delay(img.decode("utf-8"))
    result = celery_result.get(timeout=5)

    timestamp = get_timestamp(start, datetime.now())

    return PredictionOut(**result, **timestamp)


def get_timestamp(start: datetime, end: datetime):
    return {"timestamp": end.strftime("%Y-%m-%d %H:%M:%S"),
            "process_time": str(int((end - start).total_seconds() * 1000))}