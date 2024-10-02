from starlette.responses import JSONResponse
import secrets

def csrf_token_response():
    # CSRF 토큰 생성
    csrf_token = secrets.token_hex(16)
    
    # 응답 본문에 CSRF 토큰을 포함하지 않고, 쿠키에만 설정
    response = JSONResponse({"message": "CSRF token sent"})
    response.set_cookie(key="csrf_token", value=csrf_token, httponly=True)
    
    return response
