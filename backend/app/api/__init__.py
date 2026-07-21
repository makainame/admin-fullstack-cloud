from fastapi import APIRouter
from app.api import login, user, upload, excel

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(user.router)
api_router.include_router(upload.router)
api_router.include_router(excel.router)
