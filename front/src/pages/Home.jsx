import React from 'react';
import MainPost from '../components/Board/MainPost';

const Home = () => {
  return (
    <div>
      <div className='main-container'>
        <MainPost num={'1'} category = {'free'} />
        <MainPost num={'2'} category = {'news'}/>
        <MainPost num={'3'} category = {'question'}/>
        <MainPost num={'4'} category = {'test'}/>
      </div>
    </div>
  );
};

export default Home;
