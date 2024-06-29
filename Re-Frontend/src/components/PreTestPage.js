import React, {useState, useRef} from 'react';
import {useNavigate} from 'react-router-dom';
import '../PreTestPage.css';

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
          //사용자의 마이크로부터 오디오 입력 받아오기
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          mediaRecorderRef.current = new MediaRecorder(stream);
          
          //오디오 데이터 처리
          const audioChunks = [];
          mediaRecorderRef.current.ondataavailable = (event) => {
            audioChunks.push(event.data);
          };
  
          //녹음 중지 & 오디오 파일 생성
          mediaRecorderRef.current.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            setAudioURL(audioUrl);
          };
  
          //녹음 시작
          mediaRecorderRef.current.start();
          setIsRecording(true);
        } catch (err) {
          console.error('Error accessing microphone:', err);
        }
      }
      //녹음 중지
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
      <div className="pretest-page">
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
    );
  
  }

export default PreTestPage;