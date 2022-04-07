from celery import Celery

app = Celery(
    "prediction",
    broker="pyamqp://idcardadm:idcardadm@localhost//",
    backend='rpc://',
    include=['prediction.tasks']
)