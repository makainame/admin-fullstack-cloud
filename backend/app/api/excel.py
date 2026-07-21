import os
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
from app.api.deps import get_current_user
from app.core.db import get_db
from app.core.security import hash_password
from app.utils.excel_util import export_user_excel, import_user_excel
from datetime import datetime

router = APIRouter(prefix="/api/excel", tags=["Excel导入导出模块"])

# 导出用户Excel（不导出密码字段）
@router.get("/export/user")
def export_user(current_user = Depends(get_current_user)):
    excel_dir = "excel"
    if not os.path.exists(excel_dir):
        os.mkdir(excel_dir)
    db, cur = get_db()
    cur.execute("SELECT id, username, nickname, create_time FROM sys_user")
    user_data = cur.fetchall()
    db.close()
    file_name = f"用户数据_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    save_path = os.path.join(excel_dir, file_name)
    export_user_excel(user_data, save_path)
    return FileResponse(save_path, filename=file_name)

# Excel批量导入用户（密码自动加密）
@router.post("/import/user")
def import_user(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(file.file.read())
    user_list = import_user_excel(temp_path)
    db, cur = get_db()
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count = 0
    for user in user_list:
        try:
            username = user.get("用户名")
            password = hash_password("123456")  # 导入默认密码，加密存储
            nickname = user.get("用户昵称", username)
            cur.execute(
                "INSERT INTO sys_user(username,password,nickname,create_time) VALUES(%s,%s,%s,%s)",
                (username, password, nickname, create_time)
            )
            count += 1
        except Exception:
            continue
    db.commit()
    db.close()
    os.remove(temp_path)
    return {"code":200, "msg":f"导入成功，共新增{count}条用户数据"}
