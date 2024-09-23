import pymysql
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

# db연결 코드
def db_con():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT'))
    )
    
# db관리 코드
@contextmanager
def get_db_cursor():
    """데이터베이스 연결과 커서를 반환하고, 자동으로 닫음"""
    db = db_con()  # DB 연결 생성
    cursor = db.cursor()  # 커서 생성
    try:
        yield db, cursor  # 호출한 곳에서 커서와 DB를 사용할 수 있게 반환
    finally:
        # 컨텍스트 종료 시 항상 커서와 DB 연결을 닫음
        cursor.close()  # 커서 닫기
        db.close()  # DB 연결 닫기