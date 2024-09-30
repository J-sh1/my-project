from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from config.db import get_db_cursor
from config.session import SessionConfig
import uuid
import bcrypt
from dotenv import load_dotenv
import os
from starlette.responses import JSONResponse

load_dotenv()

router = APIRouter()

SECRET_SERVER_SALT = os.getenv('SERVER_PASSWORD')

# 비밀번호 해싱 함수
def hash_password(password: str) -> str:
    salted_password = password + SECRET_SERVER_SALT  # 서버 측 솔트 추가
    salt = bcrypt.gensalt()  # 솔트 생성
    hashed = bcrypt.hashpw(salted_password.encode('utf-8'), salt)  # 비밀번호 해싱
    return hashed.decode('utf-8')

# 비밀번호 검증 함수
def check_password(password: str, hashed: str) -> bool:
    salted_password = password + SECRET_SERVER_SALT  # 서버 측 솔트 추가
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(salted_password.encode('utf-8'), hashed)

# 임시
@router.get('/')
async def main() :
    print('테스트')
    return ''

# 로그인
@router.post("/login_user")
async def login(request: Request):
    data = await request.json()  # JSON 데이터 파싱
    user_id = data.get('user_id')
    user_pw = data.get('user_pw')

    print(f"[로그인 요청] ID: {user_id}, PW: {user_pw}")

    with get_db_cursor() as (db, cursor):
        try:
            # 사용자 ID로 비밀번호 해시 검색
            sql = "SELECT USER_PW, USER_IDX FROM USER_INFO WHERE USER_ID = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()

            if result and check_password(user_pw, result[0]):
                # 세션 설정 (쿠키 기반 세션 처리)
                request.session['user_id'] = user_id
                request.session['user_idx'] = result[1]
                return JSONResponse(content={'message': '로그인 성공'}, status_code=200)
            else:
                raise HTTPException(status_code=401, detail="로그인 실패")

        except Exception as e:
            print(f"[로그인 요청] 오류 발생: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

# 회원가입
@router.post("/join_user")
async def join_user(request: Request):
    data = await request.json()  # JSON 데이터 파싱
    user_id = data.get('user_id')
    user_pw = hash_password(data.get('user_pw'))  # 비밀번호 해싱
    user_name = data.get('user_name')
    user_gender = data.get('user_gender')
    user_number = data.get('user_number')
    user_idx = str(uuid.uuid4())

    print(f"Parsed data: {user_id}, {user_pw}, {user_name}, {user_gender}, {user_number}")

    if not all([user_id, user_pw, user_name, user_gender, user_number]):
        raise HTTPException(status_code=400, detail="필수 정보 누락")

    with get_db_cursor() as (db, cursor):
        try:
            sql = """
            INSERT INTO USER_INFO 
            (USER_ID, USER_PW, USER_NAME, USER_GEN, USER_NUMBER, USER_IDX)
            VALUES(%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, user_pw, user_name, user_gender, user_number, user_idx))
            db.commit()
            return JSONResponse(content={'message': 'success'}, status_code=201)

        except Exception as e:
            db.rollback()
            print(f"Error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

# 로그아웃
@router.post("/logout")
async def logout(request: Request):
    request.session.pop('user_id', None)
    request.session.pop('user_idx', None)
    return JSONResponse(content={'message': '로그아웃 성공'}, status_code=200)
