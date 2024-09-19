import { useEffect } from 'react';
import './App.css';

function App() {
  useEffect(() => {
    fetch('/api/data')
    .then(res => res.json())
    .then(data => console.log(data))
  }, [])

  return (
    <div className="App">
      <div>test중</div>
    </div>
  );
}

export default App;
