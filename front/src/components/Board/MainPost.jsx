import React from 'react'
import { Link } from 'react-router-dom'
import '../../css/MainPost.css'
import BoardItem from './BoardItem'

/*
db랑 게시판목록 연동
*/

const MainPost = ({ num, category, board = [] }) => {

    console.log('baord', board)
    
    return (
        <div className={`main-container-box box${num}`}>
            <div className='main-container-plus'>
                <Link to={`/postlist/${category}`}>더보기▶</Link>
            </div>
            <div>
                <span>분류</span>
                <span>제목</span>
                <span>{category == 'news' ? '날짜' : '추천수'}</span>
            </div>
            <div></div> {/* 밑줄 */}
            {board.length > 0 ? (
                    board.map((item, index) => (
                        <BoardItem key={index} category={category} link = {item.link} title={item.title} date={item.date} />
                    ))
                ) : (
                    <p>게시글이 없습니다.</p>
                )}
        </div>
    )
}

export default MainPost