import React from 'react'
import {Link} from 'react-router-dom'

const Header = () => {
  return (
    <div>
      <div className="">
        <Link to={'/'}>
            <span className='nav-free-post'>회원가입</span>
        </Link>
        <Link to={'/'}>
            <span className='nav-free-post'>로그인</span>
        </Link>
        <Link to={'/'}>
            <span className='nav-free-post'>로그아웃</span>
        </Link>
      </div>
      <div className="">
        <Link to={'/'}>
            <span className='nav-free-post'>자유게시판</span>
        </Link>
        <Link to={'/'}>
            <span className='nav-free-post'>최신IT기사</span>
        </Link>
        <Link to={'/'} className='logo'>
            <span className='nav-free-post'>로고</span>
        </Link>
        <Link to={'/'}>
            <span className='nav-free-post'>질문게시판</span>
        </Link>
        <Link to={'/'}>
            <span className='nav-free-post'>자유게시판</span>
        </Link>
      </div>
    </div>
  )
}

export default Header