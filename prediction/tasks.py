import base64
import io

from celery.signals import worker_init
from mine.replayed import util
from mine.replayed.engine import Detection

from prediction.worker import app

engine = None


@worker_init.connect
def initialize_model(sender=None, conf=None, **kwargs):
    model_path = util.get_config_data('system', 'model_path')

    global engine
    engine = Detection(
        number=model_path.split('/')[-1],
        path=model_path
    )

    engine.run_by_path("print_0.jpg")
    print("Complete model initialization!")


@app.task(name="by_path")
def by_path(path):
    return engine.run_by_path(path)


@app.task(name="by_file")
def by_file(img):
    img = img.encode(encoding="utf-8")
    return engine.run(io.BytesIO(base64.b64decode(img)))
