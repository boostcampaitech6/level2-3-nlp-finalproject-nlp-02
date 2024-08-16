import React, { useContext } from 'react';
import {useNavigate} from 'react-router-dom';
import { UserContext } from './UserContext';
import Calendar from "react-calendar";
import 'react-calendar/dist/Calendar.css'
import styled from "styled-components";
import '../css/Lobby.css';


const StyledCalendarWrapper = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  position: relative;
`;

const StyledCalendar = styled(Calendar)`

`;


const LobbyPage = () => {

    const { user } = useContext(UserContext);
    const navigate = useNavigate();

    const goToTestPage = () => {
        navigate('/PretestPage');
    };
    
    const goToResultPage = () => {
        navigate('/ResultPage');
    };

    return (
        <div class="lobby-page">
            <h1>Lobby Page</h1>
            {user ? (
            <div>
                <h2>Welcome, {user.name}</h2>
                <p>Email: {user.email}</p>
                <p>streak: {user.streak}</p>
            </div>
            ) : (
            <p>No user information available.</p>
            )}
            <div class="button-container">
                <button class="take-test-button" onClick={goToTestPage}>시험 응시</button>
                <button class="get-result-button" onClick={goToResultPage}>결과 보기</button>
            </div>
            <StyledCalendarWrapper>
            <StyledCalendar/>
            </StyledCalendarWrapper>
        </div> 
    );
  
  }

export default LobbyPage;