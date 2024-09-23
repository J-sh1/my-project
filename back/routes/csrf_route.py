from flask import Blueprint
from config.csrf import csrf_tokebn_res

csrf_bp = Blueprint('csrf_bp', __name__)

# CSRF 토큰을 반환하는 라우트
@csrf_bp.route('/get-csrf-token', methods=['GET'])
def get_csrf_token():
    return csrf_tokebn_res()
