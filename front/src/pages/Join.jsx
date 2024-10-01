import React, { useState } from 'react'
import { FaRegEye, FaRegEyeSlash } from "react-icons/fa"
import { Link } from 'react-router-dom'
import instance from '../config/axios'

const Join = ({csrfToken}) => {

  const [pwck, setPwck] = useState(false)
  const [id, setId] = useState('')
  const [pw, setPw] = useState('')
  const [name, setName] = useState('')
  const [gender, setGender] = useState('')
  const [number, setNumber] = useState('')
  const [idbutton, setIdbutton] = useState(true)
  const [idck, setIdck] = useState(false)

  // // 쿠키에서 CSRF 토큰을 가져오는 함수
  // const getCsrfTokenFromCookies = () => {
  //     const csrfCookie = document.cookie
  //         .split('; ')
  //         .find(row => row.startsWith('csrf_token='))
  //     return csrfCookie ? csrfCookie.split('=')[1] : ''
  // };

  // 회원가입 데이터 전송
  const joinData = async (e) => {
    e.preventDefault();
    try {
      const data = {
        user_id: id,
        user_pw: pw,
        user_name: name,
        user_gender: gender,
        user_number: number
      };
      // console.log('전송할 데이터:', data)
      // console.log('CSRF 토큰:', csrfToken)

      const res = await instance.post('/join_user', data);
      if (res.data.message === 'success') {
        alert('회원가입 완료');
        window.location.href = '/';
      } else {
        alert('회원가입 실패');
      }
    } catch (error) {
      console.error('회원가입 에러:', error)
      alert('서버 오류 발생. 다시 시도해주세요.')
    }
  }

  /** 중복확인 체크 함수 (아이디) */
  const idcheck = async (e) => {
    // console.log(id)
    if (id.length > 0) {
      setIdbutton(false)
      const data = {
        user_id : id
      }
      
      const res = await instance.post('/idcheck', data)
      if (res.data.message === '불가능') { 
        setIdck(false)
      } else if (res.data.message === '사용가능') {
        setIdck(true)
      }
    } 
  }

  return (
    <div>
      <form onSubmit={joinData}>
        <div className="">
          <Link to='/'>메인</Link>
          <div className="">
            아이디<br /><input type="text" autoFocus placeholder="아이디" onChange={(e) => { setId(e.target.value) }} />
            <button type='button' onClick={() => {idcheck(id)}}>중복확인</button>
            {idbutton ? <span></span> : idck ? <span style={{color:'blue'}}>사용가능</span> : <span style={{color:'red'}}>불가능</span>}
            <br />
            <div className="">
              비밀번호<br /><input type={!pwck ? 'password' : 'text'} placeholder="비밀번호" onChange={(e) => { setPw(e.target.value) }} />
              <button type='button' onClick={() => { setPwck(!pwck) }} tabIndex={-1}>
                {!pwck ? <FaRegEyeSlash /> : <FaRegEye />}
              </button>
            </div>
            이름<br /><input type="text" onChange={(e) => { setName(e.target.value) }} /><br />
          </div>
          <br />
          <div className="">
            <div className="">
              성별<br />
              <div className="">
                <input type="radio" name="gender" value="M" onChange={e => { setGender('M') }} />
                <label>남자</label>
              </div>
              <div className="">
                <input type="radio" name="gender" value="W" onChange={e => { setGender('W') }} />
                <label>여자</label>
              </div>
            </div>
            전화번호<br /><input type="text" onChange={(e) => { setNumber(e.target.value) }} /><br />
          </div>
          <button type="submit">회원가입</button>
        </div>
      </form>
    </div>
  );
};

export default Join;
