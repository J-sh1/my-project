import './App.css';
import { Route, Routes, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import Header from './components/Header';
import Login from './pages/Login';
import Join from './pages/Join';

function App() {

  const location = useLocation()

  /** Header 출력 안하는 페이지 설정*/
  const hiddenRoutes = ['/login', '/join']

  return (
    <div className='App'>
      {!hiddenRoutes.includes(location.pathname) && <Header />}
      <Routes>
        <Route path='/' element = {<Home/>}/>
        <Route path='/login' element = {<Login/>}/>
        <Route path='/join' element = {<Join/>}/>
      </Routes>
    </div>
  );
}

export default App;
