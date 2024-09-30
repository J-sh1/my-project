from fastapi import APIRouter
from config.csrf import csrf_token_response

router = APIRouter()

@router.get("/get-csrf-token")
async def get_csrf_token():
    return csrf_token_response()
