import pymysql
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

# 데이터베이스 연결 코드
def db_con():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT'))
    )

# 데이터베이스 관리 코드
@contextmanager
def get_db_cursor():
    db = db_con()
    cursor = db.cursor()
    try:
        yield db, cursor
    finally:
        cursor.close()
        db.close()
