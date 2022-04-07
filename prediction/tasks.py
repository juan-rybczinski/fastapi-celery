import time

from prediction.worker import app
from mine.replayed import util
from mine.replayed.engine import Detection
from utils.ml import engine, init_model


init_model()


@app.task(name="by_path")
def by_path(path):
    return engine.run_by_path(path)
    # time.sleep(3)
    # return {"prediction": "true", "probability": "100%"}
