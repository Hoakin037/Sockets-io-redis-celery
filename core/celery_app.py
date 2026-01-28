from celery import Celery

REDIS_URL = "redis://localhost:6379/0"

celery_app = Celery(
    "massenger_tasks",
    broker=REDIS_URL, # Где лежат задачи на выполнение
    backend=REDIS_URL # Где хранить результаты
)

# Автоматически ищем задачи в папке tasks
celery_app.autodiscover_tasks(['tasks'])