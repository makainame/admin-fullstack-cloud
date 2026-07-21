import os, shutil
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from app.api.deps import get_current_user
from app.core.db import get_db
from app.core.security import hash_password
from datetime import datetime

router = APIRouter(prefix="/api/user", tags=["用户管理模块"])

AVATAR_DIR = "upload/avatars"

# 分页查询用户
@router.get("/list")
def user_list(
    page: int = Query(1, description="页码"),
    size: int = Query(10, description="每页条数"),
    user_info = Depends(get_current_user)
):
    db, cur = get_db()
    cur.execute("SELECT COUNT(*) AS total FROM sys_user")
    total = cur.fetchone()["total"]
    offset = (page - 1) * size
    cur.execute("SELECT id, username, nickname, avatar, create_time FROM sys_user LIMIT %s,%s", (offset, size))
    data = cur.fetchall()
    db.close()
    return {
        "code": 200,
        "data": data,
        "total": total,
        "page": page,
        "size": size
    }

# 新增用户（支持上传头像）
@router.post("/add")
def user_add(
    username: str = Form(...),
    password: str = Form(...),
    nickname: str = Form(...),
    file: UploadFile = File(None),
    user_info = Depends(get_current_user)
):
    db, cur = get_db()
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hashed_pw = hash_password(password)

    avatar_path = None
    if file:
        avatar_path = save_avatar(file)

    cur.execute(
        "INSERT INTO sys_user(username,password,nickname,avatar,create_time) VALUES(%s,%s,%s,%s,%s)",
        (username, hashed_pw, nickname, avatar_path, create_time)
    )
    db.commit()
    db.close()
    return {"code": 200, "msg": "用户新增成功", "avatar": avatar_path}

# 修改用户（支持更换头像）
@router.post("/update")
def user_update(
    uid: int = Form(...),
    nickname: str = Form(...),
    file: UploadFile = File(None),
    user_info = Depends(get_current_user)
):
    db, cur = get_db()

    avatar_path = None
    if file:
        # 删除旧头像
        cur.execute("SELECT avatar FROM sys_user WHERE id=%s", (uid,))
        old = cur.fetchone()
        if old and old.get("avatar"):
            old_path = os.path.join(AVATAR_DIR, old["avatar"])
            if os.path.exists(old_path):
                os.remove(old_path)
        avatar_path = save_avatar(file)
        cur.execute("UPDATE sys_user SET nickname=%s, avatar=%s WHERE id=%s", (nickname, avatar_path, uid))
    else:
        cur.execute("UPDATE sys_user SET nickname=%s WHERE id=%s", (nickname, uid))

    db.commit()
    db.close()
    return {"code": 200, "msg": "用户修改成功"}

# 删除用户（同时删除头像文件）
@router.delete("/del")
def user_del(uid: int, user_info = Depends(get_current_user)):
    db, cur = get_db()
    cur.execute("SELECT avatar FROM sys_user WHERE id=%s", (uid,))
    old = cur.fetchone()
    if old and old.get("avatar"):
        old_path = os.path.join(AVATAR_DIR, old["avatar"])
        if os.path.exists(old_path):
            os.remove(old_path)
    cur.execute("DELETE FROM sys_user WHERE id=%s", (uid,))
    db.commit()
    db.close()
    return {"code": 200, "msg": "用户删除成功"}

# 单条用户详情（不返回密码）
@router.get("/detail")
def user_detail(uid: int, user_info = Depends(get_current_user)):
    db, cur = get_db()
    cur.execute("SELECT id, username, nickname, avatar, create_time FROM sys_user WHERE id=%s", (uid,))
    data = cur.fetchone()
    db.close()
    return {"code": 200, "data": data}

# ===== 头像保存工具 =====
def save_avatar(file: UploadFile) -> str:
    if not os.path.exists(AVATAR_DIR):
        os.makedirs(AVATAR_DIR)
    ext = os.path.splitext(file.filename)[1].lower()
    filename = f"avatar_{datetime.now().strftime('%Y%m%d%H%M%S%f')}{ext}"
    save_path = os.path.join(AVATAR_DIR, filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return filename
