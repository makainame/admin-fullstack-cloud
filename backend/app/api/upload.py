import os, shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.api.deps import get_current_user
from app.core.db import get_db
from datetime import datetime

# 允许上传的文件类型白名单
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".zip", ".rar"}

router = APIRouter(prefix="/api", tags=["文件上传模块"])

@router.post("/upload")
def upload(file: UploadFile = File(...), user_info = Depends(get_current_user)):
    # 文件类型校验
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型：{ext}，仅支持 {ALLOWED_EXTENSIONS}")

    save_dir = "upload"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    save_path = os.path.join(save_dir, file.filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db, cur = get_db()
    cur.execute(
        "INSERT INTO upload_file(file_name,file_path,upload_user,upload_time) VALUES(%s,%s,%s,%s)",
        (file.filename, save_path, user_info["uid"], upload_time)
    )
    db.commit()
    db.close()
    return {
        "code":200,
        "filename": file.filename,
        "path": save_path,
        "upload_time": upload_time,
        "msg": "文件上传完成"
    }

# 查询上传文件分页列表
@router.get("/upload/list")
def upload_list(
    page: int = 1,
    size: int = 10,
    user_info = Depends(get_current_user)
):
    db, cur = get_db()
    offset = (page - 1) * size
    cur.execute("SELECT * FROM upload_file ORDER BY upload_time DESC LIMIT %s,%s", (offset, size))
    data = cur.fetchall()
    cur.execute("SELECT COUNT(*) AS total FROM upload_file")
    total = cur.fetchone()["total"]
    db.close()
    return {"code":200, "data":data, "total":total, "page":page, "size":size}
