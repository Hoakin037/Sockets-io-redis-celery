import socketio
from fastapi import FastAPI
from core.sio_server import sio
from api.routes import router
import sockets.chat

def create_app():
    app = FastAPI()
    app.include_router(router)

    combined_app = socketio.ASGIApp(
        socketio_server=sio,
        other_asgi_app=app
    )

    return combined_app

app = create_app()