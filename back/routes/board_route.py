from fastapi import APIRouter
from config.db import get_db_cursor

router = APIRouter()

@router.get('/board/news')
async def get_news():
    with get_db_cursor() as (db, cursor):
        sql = ''
        cursor.execute(sql)
        news = cursor.fetchall()
    return {'news' : [{'title' : n[0], 'link' : n[1]} for n in news]}