import React, { useState, useContext, useEffect } from 'react';
import {useNavigate} from 'react-router-dom';
import { UserContext } from './UserContext';
import '../css/HistoryPage.css';
import logo from '../logo/white_logo.png'

const HistoryPage = () => {
  const { user } = useContext(UserContext);
  const [data, setData] = useState(null);

  const getResults = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/me/result/`, {
        method: 'GET',
        headers: {
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

  // 컴포넌트가 마운트될 때 API 호출
  useEffect(() => {
    getResults();
  }, []);

  return (
    <div className='container'>
      {/*헤더*/}
      <header className='header'>
        <img src={logo} alt="MOPIc 로고" style={{height: '50px'}} />
        <nav className="nav">
          <a href="/">Home</a>
          <a href="/">History</a>
          <a href="/">About</a>
          <a href="/">Log in</a>
        </nav>
      </header>

      {/*메인*/}
      <main>
        <div className='files-header'>
          <h2>Files & Folders</h2>
          <input type="text" placeholder="Search 'Files & Folders'..." />
        </div>

        <table className="file-table">
          <thead>
            <tr>
              <th>Tested Date</th>
              <th>Levels</th>
            </tr>
          </thead>

          <tbody>
            {data && data.map((item) => (
              <tr key={item.id}>
                  <td><input type="checkbox" /></td>
                  <td>{item.date}</td> {/* date 표시 */}
                  <td>{item.score}</td> {/* score 표시 */}
              </tr>
            ))}            
          </tbody>
        </table>
      </main>
    </div>
  );
};

export default HistoryPage;