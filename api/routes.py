from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def get_status():
    return {"status": "ok", "service": "messenger"}

# @router.get("/example")
# async def example(request: Request):
#     redis = request.app.state.redis - обращение к редис