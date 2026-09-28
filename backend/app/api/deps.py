from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.security import decode_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        uid = payload.get("uid")
        username = payload.get("username")
        if not uid:
            raise HTTPException(status_code=401, detail="登录失效，请重新登录")
        return {"uid": uid, "username": username}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="令牌已过期，请重新登录")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="令牌非法或过期")
