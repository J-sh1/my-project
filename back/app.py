from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from config.session import SessionConfig
from apscheduler.schedulers.background import BackgroundScheduler
from crawlers.naver_news import crawl_latest_news
from routes.user_route import router as user_router
from routes.csrf_route import router as csrf_router
from routes.board_route import router as board_router
from routes.error_route import page_not_found, internal_server_error
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# 환경 변수 로드
load_dotenv()

# 백그라운드 스케줄러 초기화
scheduler = BackgroundScheduler()

# rate limiting 설정
limiter = Limiter(key_func=lambda request: request.client.host)
app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 스케줄러 시작 함수 정의
def start_scheduler():
    print("스케줄러 초기화 중...")
    if not scheduler.running:
        print("스케줄러가 시작되었습니다.")
        crawl_latest_news()
        scheduler.add_job(crawl_latest_news, 'interval', hours=3)
        scheduler.start()
        print("스케줄러가 정상적으로 실행 중입니다:", scheduler.running)
    else:
        print("스케줄러는 이미 실행 중입니다.")

# FastAPI 이벤트 핸들러로 스케줄러 시작
@app.on_event("startup")
async def startup_event():
    start_scheduler()

# CORS 설정
CORS_ORIGIN = os.getenv('CORS_ORIGIN', '*')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션 설정
app.add_middleware(SessionMiddleware, secret_key=SessionConfig.SECRET_KEY)

# 에러 핸들러 등록
app.add_exception_handler(404, page_not_found)
app.add_exception_handler(500, internal_server_error)

# 라우터 등록
app.include_router(user_router)
app.include_router(csrf_router)
app.include_router(board_router)

# 테스트 엔드포인트
@app.get("/")
async def root():
    return {"message": "테스트"}

# Rate limited endpoint
@app.get("/limited")
@limiter.limit("5/minute")
async def limited(request: Request):  # Request 객체 추가
    return {"message": "이 경로는 1분에 5회만 요청 가능합니다."}

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
