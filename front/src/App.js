import './App.css';
import { Route, Routes, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import Header from './components/Header';
import Login from './pages/Login';
import Join from './pages/Join';
import { useEffect, useState } from 'react';
import instance from './config/axios';
import PostList from './pages/PostList';

function App() {
  const location = useLocation();

  // 숨기고 싶은 페이지 경로 설정 (로그인, 회원가입)
  const hiddenRoutes = ['/login', '/join'];

  // CSRF 토큰과 로그인 상태를 전역으로 관리
  const [csrfToken, setCsrfToken] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false); // 로그인 상태 전역 관리


  // 세션 상태 확인
  const checkSession = async () => {
    try {
      const res = await instance.get('/check-session');  // 서버에 세션 확인 요청
      if (res.data.isLoggedIn) {
        setIsLoggedIn(true);  // 세션이 있으면 로그인 상태로 설정
      } else {
        setIsLoggedIn(false);  // 세션이 없으면 로그아웃 상태로 설정
      }
    } catch (error) {
      console.error('세션 확인 실패:', error);
    }
  };

  // CSRF 토큰 가져오기
  const fetchCsrfToken = async () => {
    try {
      const response = await instance.get('/get-csrf-token');  // CSRF 토큰 서버에서 가져옴
      const csrfCookie = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrf_token='));
      const token = csrfCookie ? csrfCookie.split('=')[1] : '';
      setCsrfToken(token);
    } catch (error) {
      console.error('CSRF 토큰 가져오기 에러:', error);
    }
  };

  // 세션 상태 확인
  useEffect(() => {
    fetchCsrfToken();
    checkSession();
  }, []);

  return (
    <div className='App'>
      {/* 특정 경로에서는 Header를 숨김 */}
      {!hiddenRoutes.includes(location.pathname) && <Header isLoggedIn={isLoggedIn} setIsLoggedIn = {setIsLoggedIn} />}
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/login' element={<Login csrfToken={csrfToken} />} />
        <Route path='/join' element={<Join csrfToken={csrfToken} />} />
        <Route path='/postlist/:category' element={<PostList csrfToken={csrfToken} />} />
      </Routes>
    </div>
  );
}

export default App;
