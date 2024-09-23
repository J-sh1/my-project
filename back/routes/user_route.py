from config.db import get_db_cursor
from config.session import SessionConfig
from flask import Blueprint, request, jsonify
import uuid

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods = ['POST'])
def login():
    print('로그인')
    return '로그인'

# 회원가입
@user_bp.route('/join_user', methods=['POST'])
def join_user():
    with get_db_cursor() as (db, cursor):
        try:
            data = request.json
            print('Received data:', data)  # 요청 데이터를 출력하여 확인

            # 필드별 데이터 추출
            user_id = data.get('user_id')
            user_pw = data.get('user_pw')
            user_name = data.get('user_name')
            user_gender = data.get('user_gender')
            user_number = data.get('user_number')
            user_idx = str(uuid.uuid4())

            print('Parsed data:', user_id, user_pw, user_name, user_gender, user_number)  # 개별 필드를 확인

            # 필수 필드 체크
            if not all([user_id, user_pw, user_name, user_gender, user_number]):
                return jsonify({'error': '필수 필드가 누락되었습니다.'}), 400

            # SQL 쿼리 실행
            sql = """
            INSERT INTO USER_INFO 
            (USER_ID, USER_PW, USER_NAME, USER_GENDER, USER_NUMBER, USER_IDX)
            VALUES(%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, user_pw, user_name, user_gender, user_number, user_idx))
            db.commit()

            return jsonify({'message': 'success'}), 201
        
        except Exception as e:
            db.rollback()  # 오류 발생 시 롤백
            print('Error:', str(e))  # 발생한 오류를 출력하여 확인
            return jsonify({'error': str(e)}), 400
