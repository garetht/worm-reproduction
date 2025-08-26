import { Routes, Route } from 'react-router-dom';
import EmailList from './pages/EmailList';
import MultiEmailDetail from './pages/MultiEmailDetail';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<EmailList />} />
      <Route path="/email/:id" element={<MultiEmailDetail />} />
    </Routes>
  );
}

export default App;
