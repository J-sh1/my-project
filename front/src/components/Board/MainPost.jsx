import React from 'react'
import { Link } from 'react-router-dom'
import '../../css/MainPost.css'
import BoardItem from './BoardItem'

/*
db랑 게시판목록 연동
*/

const MainPost = ({ num, category }) => {
    return (
        <div className={`main-container-box box${num}`}>
            <div className='main-container-plus'>
                <Link to={`/postlist/${category}`}>더보기▶</Link>
            </div>
            <div>
                <span>분류</span>
                <span>제목</span>
                <span>추천수</span>
            </div>
            <div></div> {/* 밑줄 */}
            <BoardItem category ={category}/>
            <BoardItem category ={category}/>
            <BoardItem category ={category}/>
            <BoardItem category ={category}/>
            <BoardItem category ={category}/>
            <BoardItem category ={category}/>
            <BoardItem category ={category}/>
            <BoardItem category ={category}/>

        </div>
    )
}

export default MainPost