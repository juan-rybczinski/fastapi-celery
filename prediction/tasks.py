import base64
import io

from prediction.worker import app
from utils.ml import engine, init_model

init_model()


@app.task(name="by_path")
def by_path(path):
    return engine.run_by_path(path)


@app.task(name="by_file")
def by_file(img):
    img = img.encode(encoding="utf-8")
    return engine.run(io.BytesIO(base64.b64decode(img)))
