from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import api_router
import os

app = FastAPI(title="Vue后台管理系统后端接口文档")

# 全局跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录（头像、上传文件可通过 /upload/ 直接访问）
os.makedirs("upload", exist_ok=True)
app.mount("/upload", StaticFiles(directory="upload"), name="upload")

# 挂载全部业务路由
app.include_router(api_router)
