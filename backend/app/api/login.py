from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.db import get_db
from app.core.security import create_access_token, verify_password
router = APIRouter(prefix="/api", tags=["登录认证模块"])

# 登录接口，下发JWT令牌
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db, cur = get_db()
    cur.execute("SELECT * FROM sys_user WHERE username=%s", (form_data.username,))
    user = cur.fetchone()
    db.close()
    if not user:
        raise HTTPException(status_code=400, detail="账号或密码错误")

    stored_pw = user["password"]
    # 兼容处理：bcrypt哈希 → 用verify校验；明文 → 直接比较（旧数据）
    if stored_pw.startswith("$2"):
        if not verify_password(form_data.password, stored_pw):
            raise HTTPException(status_code=400, detail="账号或密码错误")
    else:
        if stored_pw != form_data.password:
            raise HTTPException(status_code=400, detail="账号或密码错误")

    token = create_access_token({"uid": user["id"], "username": user["username"]})
    return {"access_token": token, "token_type": "bearer", "user_info": user}

# 登出接口（前端清除本地token即可）
@router.post("/logout")
def logout():
    return {"msg": "登出成功，请前端清除本地Token令牌"}
