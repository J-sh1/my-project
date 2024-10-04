import React, { useEffect, useState } from 'react'
import { FaTimes, FaRegEye, FaRegEyeSlash } from 'react-icons/fa'
import { Link } from 'react-router-dom'
import instance from '../config/axios'

const Login = ({csrfToken}) => {
  const [id, setId] = useState('')
  const [idck, setIdck] = useState(false)
  const [pw, setPw] = useState('')
  const [pwck, setPwck] = useState(false)
  const [pwview, setPwview] = useState(false)

  const loginData = async (e) => {
    e.preventDefault();
    try {
      const res = await instance.post('/login_user', {
        user_id: id,
        user_pw: pw,
      });
      if (res.data.message === '로그인 성공') {
        window.location.href = '/';
      } else {
        alert('아이디 또는 비밀번호를 확인 해주세요.');
      }
    } catch (error) {
      console.error('로그인 에러:', error);
      alert('서버 에러 발생. 다시 시도 해주세요.');
    }
  }

  const Login = () => {
    const kakaoLogin = () => {
      window.location.href = 'http://localhost:5000/kakao/login';  // 백엔드에서 설정한 카카오 로그인 엔드포인트로 이동
    }
  }

  useEffect(() => {
    setIdck(id.length > 0)  
    setPwck(pw.length > 0)  
  }, [id, pw])

  return (
    <div>
      <form onSubmit={loginData}>
        <div className="">
          <label htmlFor="loginId">아이디</label>
          <input type="text" id="loginId" value={id} onChange={(e) => setId(e.target.value)} autoComplete="userid" />
          {idck && (
            <button type="button" onClick={() => {setId(''); setIdck(false)}} tabIndex={-1}>
              <FaTimes />
            </button>
          )}
          <br />
          <label htmlFor="loginPw">비밀번호</label>
          <input
            type={!pwview ? 'password' : 'text'} id="loginPw"value={pw} onChange={(e) => setPw(e.target.value)} autoComplete="password"
          />
          {pwck && (
            <button type="button" onClick={() => {setPw(''); setPwck(false)}} tabIndex={-1} >
              <FaTimes />
            </button>
          )}
          <button type="button" onClick={(e) => { e.preventDefault(); setPwview(!pwview)}} tabIndex={-1}>
            {!pwview ? <FaRegEyeSlash /> : <FaRegEye />}
          </button>
          <br />
          <button type="submit">로그인</button>
        </div>
      </form>
      <Link to="/join">
        <button type="button">회원가입</button>
      </Link>
      <br/>
      <img 
        src="https://developers.kakao.com/tool/resource/static/img/button/login/full/ko/kakao_login_medium_narrow.png" 
        alt="카카오 로그인" 
        onClick={kakaoLogin} 
        style={{ cursor: 'pointer' }}
      />
    </div>
  )
}

export default Login