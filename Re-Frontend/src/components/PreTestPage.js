import React, {useState, useRef} from 'react';
import {useNavigate} from 'react-router-dom';
import '../css/PreTestPage.css';
import logo from '../logo/white_logo.png'

function PreTestPage() {
    //사용자 음성 받기
    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorderRef = useRef(null);
    const [audioUrl, setAudioURL] = useState(null);
    const navigate = useNavigate();
  
    // eslint-disable-next-line
    // 사용자의 음성녹음 시작 & 중지
    const handleStartRecording = async () => {
      //녹음 상태 확인. isRecording이 false일 때 녹음 시작 
      if (!isRecording) {
        try {
          //사용자의 마이크로부터 오디오 입력 받아오기. {audio:true} : 오디오 입력만 요청함. await를 사용해 비동기적으로 결과를 기다림
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          //MediaRecorder : 입력 스트림을 받아 녹음 수행. stream을 인자로 전달, MediaRecorder 인스턴스 생성. 이를 mediaRecorderRef에 저장
          mediaRecorderRef.current = new MediaRecorder(stream);
          
          //오디오 데이터 처리. ondataavailable 이벤트를 통해 오디오 데이터 처리. 이벤트 발생시마다 event.data를 audioChunks 배열에 추가함
          const audioChunks = [];
          mediaRecorderRef.current.ondataavailable = (event) => {
            audioChunks.push(event.data);
          };
  
          //녹음 중지 & 오디오 파일 생성. 녹음이 중지되면 onstop 이벤트 발생. audioChunks 배열에 저장된 오디오 데이터를 Blob 객체로 변환
          //Blob을 사용해 오디오파일의 URL 생성. 생성된 URL은 setAudioUrl을 통해 상태에 저장돼 오디오 컨트롤에서 사용
          mediaRecorderRef.current.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            setAudioURL(audioUrl);
          };
  
          //녹음 시작. setIsRecording을 사용해 isRecording 상태를 true로 설정, 녹음 중임을 나타냄
          mediaRecorderRef.current.start();
          setIsRecording(true);
        } catch (err) {
          console.error('Error accessing microphone:', err);
        }
      }
      //녹음 중지. setIsRecording을 다시 false로 변경
      else {
        mediaRecorderRef.current.stop();
        setIsRecording(false);
      }
    };
  
    //다음 페이지로 넘기기
    const goToTestPage = () => {
      navigate('/testPage');
    };
  
    return (
      <div>
        {/*헤더*/}
        <header>
            <img src={logo} alt="MOPIc 로고" style={{ height: '40px' }} />
            <nav>
            <a href="#">Home</a>
            <a href="#">About</a>
            <a href="#">History</a>
            </nav>
        </header>

        {/*바깥색*/}
        <div className='outer-container'>
          {/*안쪽 사각형*/}
          <div className='inner-box'>
            <p>시험은 하루에 한 번만 볼 수 있습니다. 중도 이탈 시 데이터는 저장되지 않습니다.</p>
            <p>문제 음성은 총 두 번 들려드립니다.</p>
            <p>조용한 환경에서 응시해주세요.</p>
            <p>마이크를 허용해주시고, 아래 버튼으로 녹음하여 녹음이 제대로 되는지 확인하세요.</p>
            <p>한 번 넘어간 번호는 다시 녹음할 수 없습니다.</p>

            <div className="button-container">
              <button className="start-recording-button" onClick={handleStartRecording}>
                  {isRecording ? 'Stop Recording' : 'Start Recording'}
              </button>
              <button className="take-test-button" onClick={goToTestPage}>시험 응시</button>
            </div>
            {audioUrl && <audio src={audioUrl} controls />}
          </div>
        </div>
      </div>
    );
  
  }

export default PreTestPage;