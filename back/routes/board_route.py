from fastapi import APIRouter, HTTPException, Request
from config.db import get_db_cursor
from starlette.responses import JSONResponse
from datetime import datetime

router = APIRouter()

def convert_to_serializable(result):
    """JSON 직렬화가 가능한 형식으로 변환하는 함수."""
    serializable_result = []
    for row in result:
        serializable_row = []
        for col in row:
            if isinstance(col, datetime):  # datetime 객체는 문자열로 변환
                serializable_row.append(col.strftime('%y-%m-%d'))
            else:
                serializable_row.append(col)
        serializable_result.append(serializable_row)
    return serializable_result

@router.get('/board/news')
async def get_news():
    with get_db_cursor() as (db, cursor):
        sql = 'SELECT * FROM news_board ORDER BY BOARD_IDX DESC'
        cursor.execute(sql)
        news = cursor.fetchall()
    return {'news' : [{'title' : n[0], 'link' : n[1]} for n in news]}

@router.get('/newslist')
async def newslist(req: Request):
    with get_db_cursor() as (db, cursor):
        try:
            sql = """
            SELECT *
            FROM news_board
            ORDER BY BOARD_IDX DESC
            LIMIT 15
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            # datetime 변환
            serializable_result = convert_to_serializable(result)

            # 각 행을 처리하여 JSON으로 변환
            formatted_result = []
            for row in serializable_result:
                formatted_result.append({
                    'idx': row[0],  # 인덱스가 맞는지 확인 필요
                    'title': row[1],
                    'link': row[2],
                    'date': row[3],
                    'cat': row[4]
                })

            return JSONResponse({'result': formatted_result})
        except Exception as e:
            print(f"Error: {e}")  # 예외 로그를 출력하여 오류 파악
            raise HTTPException(status_code=400, detail=str(e))

