import json
from redis.asyncio import Redis

REDIS_URL = "redis://localhost:6379/0"

async def get_redis_client():
    return Redis.from_url(REDIS_URL, decode_responses=True)

async def save_message_to_cache(room: str, message_data: dict):
    redis = await get_redis_client()
    key = f"chat:history:{room}"
    
    # Превращаем словарь в строку JSON
    msg_json = json.dumps(message_data)
    
    # Добавляем в начало списка и сразу обрезаем до 20 элементов
    async with redis.pipeline(transaction=True) as pipe:
        await pipe.lpush(key, msg_json)
        await pipe.ltrim(key, 0, 19)
        await pipe.execute()
    await redis.aclose()

async def get_message_history(room: str):
    redis = await get_redis_client()
    key = f"chat:history:{room}"
    # Получаем все элементы списка (их там не более 20)
    messages = await redis.lrange(key, 0, -1)
    await redis.aclose()
    # Возвращаем список словарей (десериализуем обратно)
    return [json.loads(m) for m in messages]