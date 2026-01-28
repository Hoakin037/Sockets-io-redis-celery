from core.sio_server import sio
from tasks.chat_tasks import procces_new_message
from core.redis_client import save_message_to_cache, get_message_history

@sio.event
async def connect(sid: str, environ):
    print(f"User connected: {sid}")

@sio.event
async def join_room(sid: str, data: dict):
    room = data.get("room")
    await sio.enter_room(sid, room)
    # при взходе в чат отправляем пользователю историю последних 20 сообщений
    history = await get_message_history(room)
    if history:
        # Отправляем лично тому, кто вошел (sid)
        await sio.emit("chat_history", {"messages": history}, to=sid)
    await sio.emit("system_msg", {"text": f"User {sid} joined"}, room=room)
    print(f"User {sid} joined room {room}")

@sio.event
async def send_msg(sid: str, data: dict):
    room = data.get("room")
    # Логика: здесь можно вызвать функцию из services.py для сохранения в БД
    msg = data.get("message")
    
    # Сохраняем сообщение в кэш Redis
    await save_message_to_cache(room, data)
    
    # Рассылаем всем в чате
    await sio.emit("new_msg", data, room=room)

    print(f"User {sid} send msg, Task sent to Celery") 
    procces_new_message.delay(data)
    print(f"User {sid} send msg: {msg}")


@sio.event
async def disconnect(sid: str):
    print(f"User {sid} disconnected")

