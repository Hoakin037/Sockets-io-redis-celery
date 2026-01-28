from time import sleep
from core.celery_app import celery_app

@celery_app.task(name="procces_new_message")
def procces_new_message(data: dict):
    """Задача celery с имитацией обработки"""
    sleep(2)
    message_text = data.get("message")
    print(f"--- CELERY: Сообщение '{message_text}' успешно обработано ---")
    return True