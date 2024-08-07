import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';

import PreTestPage from './components/PreTestPage';
import TestPage from './components/TestPage';
import GoogleLoginPage from './components/GoogleLoginPage';
import LobbyPage from './components/LobbyPage';
import History from './components/History'

function App() { 
  return (
    <Router>
      <Routes>
        <Route path="/" element={<GoogleLoginPage />} />
        <Route path="/lobby" element={<LobbyPage />} />
        <Route path="/preTestPage" element={<PreTestPage />} />
        <Route path="/testPage" element={<TestPage />} />
        <Route path="/historyPage" element={<History />} />
        <Route path="*" element={<GoogleLoginPage />} />
      </Routes>
    </Router>
  );
}

export default App;