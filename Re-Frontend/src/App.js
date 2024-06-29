import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import PreTestPage from './components/PreTestPage';
import TestPage from './components/TestPage';

function App() { 
  return (
    <Router>
      <Routes>
        <Route path="/preTestPage" element={<PreTestPage />} />
        <Route path="/testPage" element={<TestPage />} />
        <Route path="*" element={<PreTestPage />} />
      </Routes>
    </Router>
  );
}

export default App;