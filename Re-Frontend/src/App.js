import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';

import Feedback from './components/Feedback';
import GoogleLoginPage from './components/GoogleLoginPage';
import History from './components/History';
import LobbyPage from './components/LobbyPage';
import PreTestPage from './components/PreTestPage';
import TestPage from './components/TestPage';
import UserContext from './components/UserContext';


function App() { 
  return (
    <Router>
      <Routes>
        <Route path="/" element={<GoogleLoginPage />} />
        <Route path="/lobby" element={<LobbyPage />} />
        <Route path="/preTestPage" element={<PreTestPage />} />
        <Route path="/testPage" element={<TestPage />} />
        <Route path="/historyPage" element={<History />} />
        <Route path="/feedbackPage" element={<Feedback />} />
        <Route path="/usercontextPage" element={<UserContext />} />
        <Route path="*" element={<GoogleLoginPage />} />
      </Routes>
    </Router>
  );
}

export default App;