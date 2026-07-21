"""
批量插入测试用户数据脚本
运行方式：在 backend 目录下执行 python seed_data.py
"""
import pymysql
from app.core.config import settings
import bcrypt
from datetime import datetime, timedelta

# 测试用户数据
names = ["张三", "李四", "王五", "赵六", "孙七", "周八", "吴九", "郑十",
         "刘洋", "陈静", "杨帆", "黄磊", "林涛", "何雪", "马超", "高翔",
         "梁芳", "宋明", "唐峰", "许璐", "邓超", "冯雪", "韩冰", "曹阳", "魏亮"]

# 连接到数据库
db = pymysql.connect(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME,
    charset="utf8mb4"
)
cur = db.cursor(pymysql.cursors.DictCursor)

# 检查是否已有数据
cur.execute("SELECT COUNT(*) AS total FROM sys_user")
count = cur.fetchone()["total"]
print(f"当前用户数：{count}")

if count > 20:
    print("数据已足够，无需插入")
else:
    # 直接用 bcrypt 加密密码（兼容 passlib 格式）
    hashed_pw = bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode()
    now = datetime.now()
    inserted = 0

    for i, name in enumerate(names):
        username = f"test_{i+1:02d}"
        create_time = now - timedelta(minutes=i)

        try:
            cur.execute(
                "INSERT INTO sys_user(username,password,nickname,create_time) VALUES(%s,%s,%s,%s)",
                (username, hashed_pw, name, create_time)
            )
            inserted += 1
            print(f"✅ {username} - {name}")
        except Exception as e:
            print(f"❌ {username} - {name} 跳过（{e}）")

    db.commit()
    print(f"\n🎉 共插入 {inserted} 条测试数据")

db.close()
