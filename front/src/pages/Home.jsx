import React from 'react'
import '../css/home.css'
import {Link} from 'react-router-dom'

const Home = () => {
  return (
    <div>
      <div className='main-container'>
        <div className="main-container-box box1">
          <div>
            <span>분류</span>
            <span>제목</span>
            <Link to={'/login'}>더보기▶</Link>
          </div>
          <div></div> {/* 밑줄 */}
          <div>1</div>
        </div>
        <div className="main-container-box box2">
          <div>1</div>
        </div>
        <div className="main-container-box box3">
          <div>1</div>
        </div>
        <div className="main-container-box box4">
          <div>1</div>
        </div>
      </div>
    </div>
  )
}

export default Home