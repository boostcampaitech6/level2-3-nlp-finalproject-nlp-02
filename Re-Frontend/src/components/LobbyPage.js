import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from './UserContext';
import Calendar from "react-calendar";
import moment from 'moment';
import { Img } from 'react-image';

import 'react-calendar/dist/Calendar.css';
import '../Lobby.css';

const LobbyPage = () => {
    const curDate = new Date(); // 현재 날짜
    const [value, setValue] = useState(curDate); // 클릭한 날짜 (초기값으로 현재 날짜 설정)
    const activeDate = moment(value).format('YYYY-MM-DD'); // 클릭한 날짜 (년-월-일)

    const { user } = useContext(UserContext);
    const navigate = useNavigate();

    const goToTestPage = () => {
        navigate('/PretestPage');
    };
    
    const goToResultPage = () => {
        navigate('/ResultPage');
    };

    const dayList = [
        '2024-08-17',
        '2024-08-15',
        '2024-08-13',
        '2024-08-01',
    ];

    const addContent = ({ date }) => {
        const formattedDate = moment(date).format('YYYY-MM-DD');
        const isDayInList = dayList.includes(formattedDate);
    
        return (
            <div>
                {isDayInList && (
                    <Img
                        src="/flame.svg" // public 폴더 기준으로 경로 설정
                        alt="Flame Icon"
                        className="diaryImg"
                        width={16}
                        height={16}
                    />
                )}
            </div>
        );
    };

    return (
        <div className="lobby-page">
            <header>
                <h1>
                    <img src={logo} alt="MOPIc 로고" style={{ height: '40px' }} />
                </h1>
                <nav>
                    <a href="#">Home</a>
                    <a href="#">About</a>
                    <a href="#">History</a>
                </nav>
            </header>
            <div className="content-container">
                <div className="left-side">
                    {user ? (
                        <div className="user-info">
                            <h2>Welcome, {user.name}</h2>
                            <p>Email: {user.email}</p>
                            <p>Streak: {user.streak}</p>
                        </div>
                    ) : (
                        <p>No user information available.</p>
                    )}
                    <div className="button-container">
                        <button className="get-result-button" onClick={goToResultPage}>히스토리</button>
                        <button className="take-test-button" onClick={goToTestPage}>시험 응시</button>
                    </div>
                </div>
                <div className="right-side">
                    <Calendar
                        locale="en"
                        value={value}
                        onChange={setValue} // 날짜가 선택되면 setValue 호출
                        formatDay={(locale, date) => moment(date).format('D')}
                        tileContent={addContent} // 주석 제거하여 콘텐츠 추가
                        showNeighboringMonth={false}
                        next2Label={null}
                        prev2Label={null}
                        on
                    />
                </div>
            </div>
        </div>
    );
};

export default LobbyPage;
