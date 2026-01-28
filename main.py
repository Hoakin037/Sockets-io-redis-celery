import socketio
from fastapi import FastAPI
from contextlib import asynccontextmanager # Добавляем это
from core.sio_server import sio
from api.routes import router
from core.redis_client import get_redis_client
import sockets.chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код здесь (до app.state...) выполняется при старте
    app.state.redis = await get_redis_client()
    print("Redis client initialized (lifespan)")
    
    yield # Здесь приложение "живет" и обрабатывает запросы
    
    # Код здесь (после yield) выполняется при выключении
    if hasattr(app.state, 'redis'):
        await app.state.redis.aclose()
        print("Redis client closed (lifespan)")

def create_app():
    # Передаем lifespan в конструктор FastAPI
    fastapi_app = FastAPI(lifespan=lifespan)
    fastapi_app.include_router(router)

    # Оборачиваем в Socket.IO
    combined_app = socketio.ASGIApp(
        socketio_server=sio,
        other_asgi_app=fastapi_app
    )

    return combined_app

app = create_app()