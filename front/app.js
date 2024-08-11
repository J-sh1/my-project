import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('/api/data')
      .then(response => setData(response.data.message))
      .catch(error => console.error('There was an error!', error));
  }, []);

  return (
    <div className="App">
      <h1>{data ? data : 'Loading...'}</h1>
    </div>
  );
}

export default App;
