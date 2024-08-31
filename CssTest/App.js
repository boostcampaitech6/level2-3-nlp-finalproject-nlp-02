import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="header">
        <div className="header-left">MOPIc</div>
        <div className="header-right">
          <a href="#">History</a>
          <button>Login</button>
        </div>
      </header>
      <main>
        <div className="top-container">
          <h1>You are likely to get</h1>
          <span className="result">IH</span>
        </div>
        <div className="questions">
          <ul class="tabnav-question">
            <li><a href="#tab-q1">Q1</a></li>
            <li><a href="#tab-q2">Q2</a></li>
            <li><a href="#tab-q3">Q3</a></li>
          </ul>
        </div>
          <div className="question">
            Who is your best friend? How did you meet them? How long have you known each other?
          </div>
        <div className="feedback-container">
          <ul className="tabnav-feedback">
            <li><a href="#tab-text">텍스트</a></li>
            <li><a href="#tab-audio">오디오</a></li>
          </ul>
          <div className="content">
            <div className="box coherence">
              <h2>Coherence</h2>
              <p className="description">발화 내용의 연결성<br/>전체 발화 중 동일한 말을 몇 번 반복했는지 확인한 비율은</p>
              <p className="score">낮음</p>
            </div>
            <div className="box complexity">
              <h2>Complexity</h2>
              <p className="description">문장의 복잡도<br/>문장이 모두 간단하게 구성되어 있어 내용 전달이 명확해요.<br/>하지만 복문이나 접속문을 사용한 문장을 추가하면 문장의 다양성을 더할 수 있어요.</p>
            </div>
            <div className="box grammar">
              <h2>Grammar</h2>
              <p className="description">전체 발화 중 올바른 문법 사용 비율은</p>
              <p className="score">87.27 %</p>
              <p className="example incorrect">I like to watch movie like in a week sometimes.</p>
              <p className="example correct">I like to watch a movie once a week sometimes.</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;