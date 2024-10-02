import React, { useEffect, useState } from 'react';
import MainPost from '../components/Board/MainPost';
import instance from '../config/axios';

const Home = () => {

  const [news, setNews] = useState([])

  const newsData = async () => {
    try {
      const res = await instance.get('/newslist')
      setNews(res.data.result)
    } catch (error) {
      console.error('Request error:', error)
    }
  }
  
  useEffect(() => {
    newsData()
  }, [])

  return (
    <div>
      <div className='main-container'>
        <MainPost num={'1'} category={'free'} />
        <MainPost num={'2'} category={'news'} board={news} />
        <MainPost num={'3'} category={'question'} />
        <MainPost num={'4'} category={'test'} />
      </div>
    </div>
  );
};

export default Home;
