
import './App.css';
import Header from './views/Header';
import { useRoutes } from 'react-router-dom';
import router from './utils/router';

function App() {
  return (
    <div className="App">
      <Header></Header>
      {useRoutes(router)}
    </div>
  );
}

export default App;
