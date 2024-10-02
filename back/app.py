from fastapi import FastAPI, BackgroundTasks
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
from contextlib import asynccontextmanager

# 환경 변수 로드
load_dotenv()

# 백그라운드 스케줄러 초기화
scheduler = BackgroundScheduler()

# 스케줄러 시작 함수 정의
def start_scheduler():
    print("스케줄러 초기화 중...")
    if not scheduler.running:
        print("스케줄러가 시작되었습니다.")
        # 서버 시작 시 즉시 한 번 크롤링 실행
        crawl_latest_news()
        # 이후 3시간마다 실행
        scheduler.add_job(crawl_latest_news, 'interval', hours=3)  # 3시간마다 실행
        scheduler.start()
        print("스케줄러가 정상적으로 실행 중입니다:", scheduler.running)
    else:
        print("스케줄러는 이미 실행 중입니다.")

# Lifespan 이벤트 핸들러 정의
@asynccontextmanager
async def lifespan_context(app: FastAPI):
    print("서버가 시작되었습니다. 스케줄러 실행 준비 중...")
    start_scheduler()  # 서버 시작 시 스케줄러 실행
    yield
    print("서버가 종료됩니다. 스케줄러를 종료합니다.")
    scheduler.shutdown()  # 서버 종료 시 스케줄러 종료

# FastAPI 앱 초기화
app = FastAPI(lifespan=lifespan_context)

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

# 에러 핸들러 등록 (error_route로 분리)
app.add_exception_handler(404, page_not_found)
app.add_exception_handler(500, internal_server_error)

# FastAPI의 라우터 사용
app.include_router(user_router)
app.include_router(csrf_router)
app.include_router(board_router)

# 테스트 엔드포인트
@app.get("/")
async def root():
    print("테스트")
    return {"message": "테스트"}

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
