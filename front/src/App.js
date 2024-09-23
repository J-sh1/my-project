import './App.css';
import { Route, Routes, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import Header from './components/Header';
import Login from './pages/Login';
import Join from './pages/Join';
import { useEffect, useState } from 'react';
import instance from './config/axios'

function App() {

  const location = useLocation()

  /** Header 출력 안하는 페이지 설정*/
  const hiddenRoutes = ['/login', '/join']

  const [csrfToken, setCsrfToken] = useState('')

  useEffect(() => {
    const fetchCsrfToken = async () => {
      try {
        const response = await instance.get('/get-csrf-token');  // CSRF 토큰을 서버에서 가져옴
        const csrfCookie = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrf_token='));
        const token = csrfCookie ? csrfCookie.split('=')[1] : '';
        setCsrfToken(token);
        // console.log('CSRF 토큰 가져오기 성공:', token);
      } catch (error) {
        // console.error('CSRF 토큰 가져오기 에러:', error);
      }
    };
    fetchCsrfToken();
  }, [])

  return (
    <div className='App'>
      {!hiddenRoutes.includes(location.pathname) && <Header />}
      <Routes>
        <Route path='/' element = {<Home/>}/>
        <Route path='/login' element = {<Login csrfToken={csrfToken}/>} />
        <Route path='/join' element = {<Join csrfToken={csrfToken}/>} />
      </Routes>
    </div>
  );
}

export default App;
