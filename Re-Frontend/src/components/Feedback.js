import React, { useState } from 'react';
import '../css/Feedback.css';
import logo from '../logo/white_logo.png'

function App() {
  const [activeQuestion, setActiveQuestion] = useState('Q1');
  const [activeSubTab, setActiveSubTab] = useState('textFeedback');

  const questions = {
    Q1: {
      question: "What do you like to do in your free time?",
      textFeedback: { /*사용자 개인화*/
        complexity: "문장이 모두 간단하게 구성되어 있어 내용 전달이 명확했으나, 복문이나 긴 문장을 사용하면 한층 풍부한 문장의 다양성을 더할 수 있어요.",
        grammarScore: "87.27 %",
        grammarExample: "I like to watch a movie once a week sometimes.",
        coherenceScore: "낮음"
      },
      audioFeedback: { /*사용자 개인화*/
        pronunciation: "66.83 %",
        mlr: "4 개",
        pr: "39.0 %"
      }
    },
    Q2: {
      question: "Second question goes here",
      textFeedback: { /*사용자 개인화*/
        complexity: "문장이 모두 간단하게 구성되어 있어 내용 전달이 명확했으나, 복문이나 긴 문장을 사용하면 한층 풍부한 문장의 다양성을 더할 수 있어요.",
        grammarScore: "80.27 %",
        grammarExample: "I like to watch a movie once a week sometimes.",
        coherenceScore: "낮음"
      },
      audioFeedback: { /*사용자 개인화*/
        pronunciation: "66.83 %",
        mlr: "3.33 개",
        pr: "39.0 %"
      }
    },
    Q3: {
      question: "Third question goes here",
      textFeedback: { /*사용자 개인화*/
        complexity: "문장이 모두 간단하게 구성되어 있어 내용 전달이 명확했으나, 복문이나 긴 문장을 사용하면 한층 풍부한 문장의 다양성을 더할 수 있어요.",
        grammarScore: "90.27 %",
        grammarExample: "I like to watch a movie once a week sometimes.",
        coherenceScore: "낮음"
      },
      audioFeedback: { /*사용자 개인화*/
        pronunciation: "66.83 %",
        mlr: "3.33 개",
        pr: "39.0 %"
      }
    }
  };

  const handleTabClick = (tab) => {
    setActiveQuestion(tab);
    setActiveSubTab('textFeedback'); // Reset sub-tab to textFeedback when switching main tabs
  };

  const handleSubTabClick = (subTab) => {
    setActiveSubTab(subTab);
  };

  const currentQuestion = questions[activeQuestion];

  return (
    <div>
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

      <main>
        <div className="feedback-container">
          <h1>You are likely to get</h1>
          <h2>IH</h2> {/* 사용자 개인화 */}
          
          <div className="tabs">
            {Object.keys(questions).map((tab) => (
              <button
                key={tab}
                className={`tab-button ${activeQuestion === tab ? 'active' : ''}`}
                onClick={() => handleTabClick(tab)}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="tab-content active">
            <div className="question-sentence">
              <h3>{currentQuestion.question}</h3>
            </div>

            <div className="feedback-box">
              <div className="sub-tabs">
                <button
                  className={`sub-tab-button ${activeSubTab === 'textFeedback' ? 'active' : ''}`}
                  onClick={() => handleSubTabClick('textFeedback')}
                >
                  Text
                </button>
                <button
                  className={`sub-tab-button ${activeSubTab === 'audioFeedback' ? 'active' : ''}`}
                  onClick={() => handleSubTabClick('audioFeedback')}
                >
                  Audio
                </button>
              </div>

              {activeSubTab === 'textFeedback' && (
                <div className="sub-tab-content active">
                  <div className="feedback-row">
                    <div className="feedback-category">
                      <div className="feedback-section">
                        <h3>Coherence</h3>
                        <p className="desc">Coherence는 주제에 맞는 흐름을 유지하며 명확하게 전달되는지 확인하는 요소입니다.</p>
                        <p className="output score">{currentQuestion.textFeedback.coherenceScore}</p>
                      </div>
                    </div>
                    <div className="feedback-category">
                      <div className="feedback-section">
                        <h3>Complexity</h3>
                        <p className="desc">complexity 설명</p>
                        <p className="output sentence">{currentQuestion.textFeedback.complexity}</p>
                      </div>
                    </div>
                  </div>
                  <div className="feedback-row">
                    <div className="feedback-category grammar">
                      <div className="feedback-section">
                        <h3>Grammar</h3>
                        <p className="desc">전체 발화 중 올바른 문법 사용 비율은</p>
                        <p className="output score">{currentQuestion.textFeedback.grammarScore}</p>
                        <p>{currentQuestion.textFeedback.grammarExample}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeSubTab === 'audioFeedback' && (
                <div className="sub-tab-content active">
                  <div className="feedback-row">
                    <div className="feedback-category">
                      <div className="feedback-section">
                        <h3>Pronunciation</h3>
                        <p className="desc">사용자의 발음이 원어민과 얼마나 유사한 지 보여주는 지표입니다.</p>
                        <p class="desc">전체 발화 중 잘못된 발음 없이 명확하게 발음한 비율은</p>
                        <p className="output score">{currentQuestion.audioFeedback.pronunciation}</p>
                      </div>
                    </div>
                    <div className="feedback-category">
                      <div className="feedback-section">
                        <h3>Mean Length of Run (MLR)</h3>
                        <p className="desc">사용자가 연속적으로 발음한 평균 단어 수입니다. MLR이 높을수록 보다 유창함을 보여주는 지표입니다.</p>
                        <p class="desc">연속으로 발화한 평균 단어 수는</p>
                        <p className="output score">{currentQuestion.audioFeedback.mlr}</p>
                      </div>
                    </div>
                  </div>
                  <div className="feedback-row">
                    <div className="feedback-category pr">
                      <div className="feedback-section">
                        <h3>Pause Rate (PR)</h3>
                        <p className="desc">PR 설명 어쩌구</p>
                        <p class="desc">전체 발화 중 pause 비율은</p>
                        <p className="output score">{currentQuestion.audioFeedback.pr}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
