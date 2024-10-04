from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from config.db import get_db_cursor
from config.session import SessionConfig
from starlette.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uuid
import bcrypt
import requests

load_dotenv()

router = APIRouter()

SECRET_SERVER_SALT = os.getenv('SERVER_PASSWORD')

# JWT 설정 클래스
class Settings(BaseModel):
    authjwt_secret_key: str = "your_jwt_secret_key"

@AuthJWT.load_config
def get_config():
    return Settings()

# 비밀번호 해싱 함수
def hash_password(password: str) -> str:
    salted_password = password + SECRET_SERVER_SALT
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(salted_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# 비밀번호 검증 함수
def check_password(password: str, hashed: str) -> bool:
    salted_password = password + SECRET_SERVER_SALT
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(salted_password.encode('utf-8'), hashed)

# 로그인
@router.post("/login_user")
async def login(req: Request, Authorize: AuthJWT = Depends()):
    data = await req.json()
    user_id = data.get('user_id')
    user_pw = data.get('user_pw')

    print(f"[로그인 요청] ID: {user_id}, PW: {user_pw}")

    with get_db_cursor() as (db, cursor):
        try:
            sql = "SELECT USER_PW, USER_IDX FROM USER_INFO WHERE USER_ID = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()

            if result and check_password(user_pw, result[0]):
                # JWT 생성
                access_token = Authorize.create_access_token(subject=user_id)
                
                # 세션에 user_id 저장
                req.session['user_id'] = user_id
                req.session['user_idx'] = result[1]

                return JSONResponse(content={'message': '로그인 성공', 'access_token': access_token}, status_code=200)
            else:
                raise HTTPException(status_code=401, detail="로그인 실패")

        except Exception as e:
            print(f"[로그인 요청] 오류 발생: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))


# Kakao OAuth 설정
KAKAO_CLIENT_ID = os.getenv('KAKAO_KEY')
KAKAO_REDIRECT_URI = "http://localhost:5000/kakaologin"
KAKAO_AUTH_URL = f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"

# 카카오 로그인 라우트
@router.get("/kakao/login")
def kakao_login():
    return RedirectResponse(KAKAO_AUTH_URL)

# 카카오 인증 콜백 라우트
@router.get("/kakao/callback")
def kakao_callback(request: Request):
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail="인증 실패")

    token_url = "https://kauth.kakao.com/oauth/token"
    token_data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }

    # 카카오로부터 토큰 받기
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="토큰 발급 실패")

    # 사용자 정보 받기
    user_info_url = "https://kapi.kakao.com/v2/user/me"
    user_info_response = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"})
    user_info = user_info_response.json()

    if not user_info.get("id"):
        raise HTTPException(status_code=400, detail="사용자 정보 조회 실패")

    # 카카오 사용자 정보로 로그인 처리 (DB 연동 등 추가)
    kakao_id = user_info.get("id")
    kakao_email = user_info.get("kakao_account", {}).get("email")

    # 로그인 로직 추가 (DB에 사용자 정보 저장, 세션 설정, JWT 발급 등)
    # 예: req.session['user_id'] = kakao_id
    
    return {"message": "카카오 로그인 성공", "kakao_id": kakao_id, "email": kakao_email}



# routes/user_route.py 파일에 있는 idcheck 라우트
@router.post('/idcheck')
async def idcheck(req: Request):
    data = await req.json()
    user_id = data.get('user_id')
    
    with get_db_cursor() as (db, cursor):
        try:
            sql = """
            SELECT COUNT(*)
            FROM USER_INFO
            WHERE USER_ID = %s
            """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            
            if result[0] > 0:
                message = '불가능'  # ID가 이미 존재하므로 사용 불가능
            else:
                message = '사용가능'  # ID가 없으므로 사용 가능
            
            return JSONResponse(content={'message': message})
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

# 로그아웃
@router.post("/logout")
async def logout(req: Request):
    req.session.pop('user_id', None)
    req.session.pop('user_idx', None)
    return JSONResponse(content={'message': '로그아웃 성공'}, status_code=200)

# 세션확인
@router.get('/check-session')
async def check_session(req: Request):
    user_id = req.session.get('user_id')  # 세션에서 user_id를 확인
    if user_id:
        return JSONResponse(content={'isLoggedIn': True})
    else:
        return JSONResponse(content={'isLoggedIn': False})
    
