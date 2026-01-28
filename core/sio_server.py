from socketio import AsyncServer, AsyncRedisManager 
REDIS_URL = "redis://localhost:6379/0"

manager = AsyncRedisManager(REDIS_URL)

sio = AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    client_manager=manager
)