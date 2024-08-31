import React, { useState, useContext } from 'react';
import { GoogleLogin } from "@react-oauth/google";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { jwtDecode } from 'jwt-decode';  // 중괄호 없이 임포트
import {  useNavigate, Link } from 'react-router-dom';  // Router를 추가

import logo from '../logo/white_logo.png'
import '../css/Welcome.css';  // CSS 파일을 import


const Welcome = () => {
  const clientId = "YOUR_CLIENT_ID"; // 본인의 Google Client ID로 대체하세요.
  const navigate = useNavigate();

  const handleLogin = async (credentialResponse) => {
    const token = credentialResponse.credential;
    const decoded = jwtDecode(token);
    console.log(decoded);

    try {
      const response = await fetch('http://mopic.today:8888/api/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token }),
      });
      if (response.ok) {
        const data = await response.json();
        console.log(data);
        navigate('/lobby');
      } else {
        console.error('Login verification failed');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <GoogleOAuthProvider clientId={clientId}>
      <div className="login-page">
        <header>
          <h1>
            <img src={logo} alt="MOPIc 로고" style={{ height: '40px' }} />
          </h1>
          <nav>
            <Link to="/home">Home</Link>
            <Link to="/about">About</Link>
            <Link to="/history">History</Link>
          </nav>
        </header>

        <main>
          <div className="content">
            <p>👨‍🎓 시험 응시료도 만만찮고, 내가 잘하고 있는지도 모르겠어<br />
              취업 시장에서 날이 갈수록 중요해지는 영어 시험<br />
              5분 정도의 테스트로 내가 어느 정도인지 알아보고, 앞으로 어떻게 해야 할지 파악해 보자!<br />
              하루에 딱 5분! 어떤 주제가 나와도 탄탄한 기본기를 쌓으려면? 모픽으로!</p>
            <p>지금 바로 로그인하기!</p>
            <GoogleLogin
              onSuccess={handleLogin}
              onError={() => {
                console.log("Login Failed");
              }}
            />
          </div>
          <div className="side-content">
            <div className="logo">
              <img src={logo} alt="MOPIc 로고" />
            </div>
          </div>
        </main>

        <footer>
          <p>&copy; 2024 Mopic. All rights reserved.</p>
        </footer>
      </div>
    </GoogleOAuthProvider>
  );
};

export default Welcome;