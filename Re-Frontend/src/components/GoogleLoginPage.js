import React, { useContext } from 'react';
import { GoogleLogin } from "@react-oauth/google";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from 'react-router-dom';
import { UserContext } from './UserContext';

const GoogleLoginPage = () => {
  const clientId = "373399218972-csivbh2naa28dtnjv44jnv069br2ravi.apps.googleusercontent.com";
  const navigate = useNavigate();
  const { setUser } = useContext(UserContext);

  const handleLogin = async (credentialResponse) => {
    const token = credentialResponse.credential;
    const decoded = jwtDecode(token);
    setUser(decoded);
    console.log(decoded);

    try {
      const response = await fetch('http://localhost:8000/api/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token }),
      });
      if (response.ok) {
        const data = await response.json();
        console.log(data);
        // 로그인 성공 후 LobbyPage로 이동
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
      <div>
        <h1>Mopic Login</h1>
        <GoogleLogin
          onSuccess={handleLogin}
          onError={() => {
            console.log("Login Failed");
          }}
        />
      </div>
    </GoogleOAuthProvider>
  );
};

export default GoogleLoginPage;