from datetime import datetime, timedelta
import jwt
import bcrypt
from app.core.config import settings

# ===== JWT 令牌工具 =====

# 生成登录令牌
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=settings.JWT_EXPIRE_HOUR)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

# 解析校验令牌
def decode_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

# ===== 密码加密工具 =====

# 加密密码
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# 校验密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
