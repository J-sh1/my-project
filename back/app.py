from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from config.session import SessionConfig
from routes.user_route import router as user_router
from routes.csrf_route import router as csrf_router

load_dotenv()

app = FastAPI()

# CORS 설정
CORS_ORIGIN = os.getenv('CORS_ORIGIN', '*')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션 설정 (SessionMiddleware로 세션 처리)
app.add_middleware(SessionMiddleware, secret_key=SessionConfig.SECRET_KEY)

# FastAPI의 라우터 사용
app.include_router(user_router)
app.include_router(csrf_router)

# 에러 핸들러 등록 (FastAPI에서는 exception_handler 사용)
@app.exception_handler(404)
async def page_not_found(request: Request, exc):
    return JSONResponse(status_code=404, content={"error": "Page not found"})

@app.exception_handler(500)
async def internal_server_error(request: Request, exc):
    return JSONResponse(status_code=500, content={"error": "Internal server error"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)



# 개발용 SSL 실행 예제 (uvicorn에서는 별도 설정 필요)
# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=5000, ssl_keyfile="path/to/key", ssl_certfile="path/to/cert", debug=True)
