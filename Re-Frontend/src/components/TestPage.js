import React, {useState, useRef, useEffect} from 'react';
import '../TestPage.css';
import {useNavigate} from 'react-router-dom';
import logo from '../logo/white_logo.png'

 
function TestPage() {
    const [activeButton, setActiveButton] = useState(null);
    //버튼 클릭 상태 추가
    const [clickedButtons, setClickedButtons] = useState({});
    //Replay 버튼 클릭 상태 추가
    const [replayClicked, setReplayClicked] = useState(false);
    //녹음 상태 추가
    const [isRecording, setIsRecording] = useState(false);
    const [recordingStarted, setRecordingStarted] = useState(false);
    const audioRef = useRef(null);
    const mediaRecorderRef = useRef(null);
    //오디오 청크 저장
    const audioChunksRef = useRef([]);


    const playAudio = (buttonNumber) => {
        let audioSrc;
        switch (buttonNumber) {
            case 1:
                audioSrc = require('../question_1.wav');
                break;
            case 2:
                audioSrc = require('../question_2.wav');
                break;
            case 3:
                audioSrc = require('../question_3.wav');
                break;
            default:
                return;
        }
        if (audioRef.current) {
            audioRef.current.src = audioSrc;
            audioRef.current.play();
        }
    };

    const handleButtonClick = (buttonNumber) => {
        //버튼이 처음 클릭된 경우에만 음성 출력
        if (!clickedButtons[buttonNumber]) {
            setActiveButton(buttonNumber);
            //오디오 재생함수 호출
            playAudio(buttonNumber);
            //클릭 상태 업데이트
            setClickedButtons(prevState => ({...prevState, [buttonNumber]: true}));
            //Replay 버튼 상태 초기화
            setReplayClicked(false);
        }
    };
    
    const replayAudio = () => {
        if (activeButton !== null && !replayClicked) {
            playAudio(activeButton);
            setReplayClicked(true);
        }
    };

    const startRecording = async () => {
        if (!isRecording && !recordingStarted) {
            setIsRecording(true);
            // recordingStarted 상태를 제거, 매번 녹음 가능하도록 수정
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorderRef.current = new MediaRecorder(stream);
                mediaRecorderRef.current.ondataavailable = (event) => {
                    audioChunksRef.current.push(event.data);
                };
                mediaRecorderRef.current.onstop = () => {
                    const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
                    audioChunksRef.current = [];
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = audioUrl;
                    a.download = 'recording.wav';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(audioUrl);
                };
                mediaRecorderRef.current.start();
            } catch (err) {
                console.error("Error accessing media devices.", err);
                setIsRecording(false);
            }
        }
    };

    const stopRecording = () => {
        if (isRecording && mediaRecorderRef.current) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);

            //녹음 중지 클릭 시 다음 문제 자동재생
            if (activeButton === 1) {
                handleButtonClick(2);
            } else if (activeButton === 2) {
                handleButtonClick(3);
            }
        }
    };

    useEffect(() => {
        return () => {
            if (mediaRecorderRef.current) {
                mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
            }
        };
    }, []);

    return (
    <div>
        {/*헤더*/}
        <div className='header'>
            <img src={logo} alt="MOPIc 로고" style={{height: '50px'}} />

        </div>

    {/*바깥색*/}
    <div className='outer-container'>
        <div className="inner-box">
            <h1>Daily Test</h1>
            <div className="character-container">
                <img src={require("../logo/AVA.png")} alt="AVA"></img>
                <p style={{color: '#5F5F5F'}}>문제를 두 번 들으신 후 바로 녹음을 시작해주세요.</p>
            </div>
            
            <div className="button-container">
                <button onClick={() => handleButtonClick(1)}>1</button>
                <button onClick={() => handleButtonClick(2)}>2</button>
                <button onClick={() => handleButtonClick(3)}>3</button>
            </div>

            {activeButton && (
                <div className="conditional-buttons">
                    {activeButton!==3 && (<button className="replay-button" onClick={replayAudio}>Replay</button>)}
                    <button className="next-button" onClick={isRecording ? stopRecording : startRecording}>
                        {isRecording ? '녹음 중지' : '녹음 시작'}
                    </button>
                </div>
            )}
            <audio ref={audioRef} />
        </div>
        </div>
    </div>
    
    );
}

export default TestPage;
