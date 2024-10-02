import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import instance from '../config/axios'

const Header = ({isLoggedIn, setIsLoggedIn}) => {
  // const [isLoggedIn, setIsLoggedIn] = useState(false)  // 로그인 여부 상태

  // // 세션 확인 함수
  // const checkSession = async () => {
  //   try {
  //     const res = await instance.get('/check-session')  // 서버에 세션 확인 요청
  //     if (res.data.isLoggedIn) {
  //       setIsLoggedIn(true)  // 세션이 있으면 로그인 상태로 설정
  //     } else {
  //       setIsLoggedIn(false)  // 세션이 없으면 로그아웃 상태로 설정
  //     }
  //   } catch (error) {
  //     console.error('세션 확인 실패:', error)
  //   }
  // }

  // // 컴포넌트가 마운트될 때 세션 확인
  // useEffect(() => {
  //   checkSession()
  // }, [])

  // 로그아웃 함수
  const logout = async () => {
    try {
      const res = await instance.post('/logout')
      if (res.data.message === '로그아웃 성공') {
        setIsLoggedIn(false)  // 로그아웃 후 상태 변경
        window.location.href = '/'
      }
    } catch (error) {
      console.error('로그아웃 실패:', error)
    }
  }

  return (
    <div>
      <div className="">
        {isLoggedIn ? (
          // 로그인 상태일 때 로그아웃 버튼만 표시
          <span onClick={logout} className='nav-free-post'>로그아웃</span>
        ) : (
          // 로그아웃 상태일 때 회원가입, 로그인 버튼 표시
          <>
            <Link to={'/join'}>
              <span className='nav-free-post'>회원가입</span>
            </Link>
            <Link to={'/login'}>
              <span className='nav-free-post'>로그인</span>
            </Link>
          </>
        )}
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
