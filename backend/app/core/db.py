import pymysql
from app.core.config import settings
def get_db():
    db = pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        charset="utf8mb4"
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor
