import React, { useState, useContext } from 'react';
import {useNavigate} from 'react-router-dom';
import { UserContext } from './UserContext';

const HistoryPage = () => {
  const { user, date } = useContext(UserContext);
  const [data, setData] = useState(null);

  const getResults = async (date) => {
    try {
      const response = await fetch(`http://localhost:8000/api/me/result/`, {
        method: 'GET',
        headetrs: {
          'Content-Type': 'application/json',
        }
      });
      if (response.ok) {
        const data = await response.json();
        console.log(data);
        setData(data);
      }
    } catch (error) {
        console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>목록</h1>
      <div>
        {data ? (
          <div>
            <h2>결과:</h2>
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </div>
        ) : (
          <p>데이터가 없습니다</p>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;