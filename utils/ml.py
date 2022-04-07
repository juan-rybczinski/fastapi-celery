import logging

from mine.replayed import util
from mine.replayed.engine import Detection

model_path = util.get_config_data('system', 'model_path')

engine = Detection(
    number=model_path.split('/')[-1],
    path=model_path
)


def init_model():
    engine.run_by_path("print_0.jpg")
    print("Complete model initialization!")