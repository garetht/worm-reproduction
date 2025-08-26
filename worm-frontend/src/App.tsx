import { Routes, Route } from 'react-router-dom';
import EmailList from './pages/EmailList';
import EmailDetail from './pages/EmailDetail';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<EmailList />} />
      <Route path="/email/:id" element={<EmailDetail />} />
    </Routes>
  );
}

export default App;