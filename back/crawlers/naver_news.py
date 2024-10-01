import requests
from bs4 import BeautifulSoup as bs
from config.db import get_db_cursor
import pymysql  # MySQL 사용 시 필요

def crawl_latest_news():
    try:
        print('크롤링시작')
        url = "https://news.naver.com/section/105"  # 뉴스 사이트 URL
        response = requests.get(url)
        if response.status_code != 200:
            print(f"크롤링 실패, 상태 코드: {response.status_code}")
            return []

        soup = bs(response.content, "lxml")

        # 뉴스 제목과 링크 추출
        articles = []
        for item in soup.select("div.sa_text>a"):
            title = item.get_text().strip().replace("\\", "")
            link = item.get("href")
            # print(f"크롤링된 뉴스: {title} - {link}")
            articles.append({"title": title, "link": link})
        
        # 크롤링이 완료된 후 DB에 저장
        save_news_to_db(articles)

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")

    
def save_news_to_db(articles):
    with get_db_cursor() as (db, cursor):
        for article in articles:
            try:
                # 중복된 값이 있을 경우 DB에서 UNIQUE 제약 조건에 의해 오류 발생
                sql = """
                    INSERT INTO news_board (title, link) 
                    VALUES (%s, %s)
                """
                cursor.execute(sql, (article['title'], article['link']))
                db.commit()
                print(f"DB에 저장된 뉴스: {article['title']} - {article['link']}")
            except Exception as e:
                # 다른 오류 발생 시 처리
                # print(f"DB 저장 중 오류 발생: {e}")
                db.rollback()  # 오류 발생 시 트랜잭션 롤백
