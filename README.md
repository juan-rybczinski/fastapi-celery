# fastapi-celery

## mine-replayed 설치
```commandline
cd whl
pip install mine_replayed-<version>-py3-none-any.whl
```

## Celery 실행 시
Tensorflow 사용 시에는 --pool=threads 옵션을 사용해야 함
```commandline
celery -A prediction.worker worker -c <worker_num> --pool=threads --loglevel=INFO
```