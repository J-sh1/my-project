# FastAPI에서는 CSRF 보호가 기본적으로 제공되지 않으므로 생략하거나
# 다른 방식으로 구현해야 합니다.
from starlette.responses import JSONResponse

def csrf_token_response():
    # CSRF 토큰을 생성하고 응답에 설정하는 로직
    return JSONResponse({"message": "CSRF token sent"})
