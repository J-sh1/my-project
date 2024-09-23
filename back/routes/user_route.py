from config.db import get_db_cursor
from config.session import SessionConfig
from flask import Blueprint, request, jsonify, session
import uuid
import bcrypt
from dotenv import load_dotenv
import os


user_bp = Blueprint('user', __name__)

load_dotenv()

SECRET_SERVER_SALT = os.getenv('SERVER_PASSWORD')

# 비밀번호를 해싱하는 함수
def hash_password(password):
    salted_password = password + SECRET_SERVER_SALT  # 서버 측 문자열을 비밀번호에 추가
    salt = bcrypt.gensalt()  # bcrypt의 솔트 생성
    hashed = bcrypt.hashpw(salted_password.encode('utf-8'), salt)  # 해싱
    # print(f"[회원가입] SECRET_SERVER_SALT: {SECRET_SERVER_SALT}")  # 로그 추가
    # print(f"[회원가입] 해싱된 비밀번호: {hashed.decode('utf-8')}")  # 로그 추가
    return hashed

# 입력한 비밀번호가 해시된 비밀번호와 일치하는지 확인하는 함수
def check_password(password, hashed):
    salted_password = password + SECRET_SERVER_SALT  # 서버 측 문자열을 비밀번호에 추가
    # 데이터베이스에서 가져온 해시된 비밀번호는 문자열이므로, 이를 바이트 형식으로 변환
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')  # 문자열을 바이트로 변환
    return bcrypt.checkpw(salted_password.encode('utf-8'), hashed)

# 로그인 함수
@user_bp.route('/login_user', methods=['POST'])
def login():
    with get_db_cursor() as (db, cursor):
        try:
            data = request.json
            user_id = data.get('user_id')
            user_pw = data.get('user_pw')

            print(f"[로그인 요청] ID: {user_id}, PW: {user_pw}")

            # 사용자 ID로 비밀번호 해시 검색
            sql = "SELECT USER_PW, USER_IDX FROM USER_INFO WHERE USER_ID = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()

            # 비밀번호 비교
            if result and check_password(user_pw, result[0]):
                session['user_id'] = user_id
                session['user_idx'] = result[1]
                return jsonify({'message': '로그인 성공'}), 200
            else:
                print("[로그인 요청] 비밀번호 불일치")
                return jsonify({'message': '로그인 실패'}), 401
        
        except Exception as e:
            print(f"[로그인 요청] 오류 발생: {str(e)}")
            return jsonify({'error': str(e)}), 400




# 회원가입
@user_bp.route('/join_user', methods=['POST'])
def join_user():
    with get_db_cursor() as (db, cursor):
        try:
            data = request.json
            print('Received data:', data)  # 요청 데이터를 출력하여 확인

            # 필드별 데이터 추출
            user_id = data.get('user_id')
            user_pw = hash_password(data.get('user_pw'))
            user_name = data.get('user_name')
            user_gender = data.get('user_gender')
            user_number = data.get('user_number')
            user_idx = str(uuid.uuid4())

            print('Parsed data:', user_id, user_pw, user_name, user_gender, user_number)  # 개별 필드를 확인

            # 필수 필드 체크
            if not all([user_id, user_pw, user_name, user_gender, user_number]):
                return jsonify({'error': '필수 정보 누락되었습니다.'}), 400

            # SQL 쿼리 실행
            sql = """
            INSERT INTO USER_INFO 
            (USER_ID, USER_PW, USER_NAME, USER_GEN, USER_NUMBER, USER_IDX)
            VALUES(%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, user_pw, user_name, user_gender, user_number, user_idx))
            db.commit()

            return jsonify({'message': 'success'}), 201
        
        except Exception as e:
            db.rollback()  # 오류 발생 시 롤백
            print('Error:', str(e))  # 발생한 오류를 출력하여 확인
            return jsonify({'error': str(e)}), 400
     
# 로그아웃   
@user_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # 세션에서 user_id 삭제
    session.pop('user_idx', None)  # 세션에서 user_idx 삭제
    return jsonify({'message': '로그아웃 성공'}), 200
