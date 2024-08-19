import React,{useEffect, useRef, useState} from 'react';
import '../css/FeedbackPage.css'
import logo from '../logo/white_logo.png'


function FeedbackPage() {
    const [activeQuestion, setActiveQuestion] = useState(null);
    const [activeTab, setActiveTab] = useState('Text');
    const tabButtonsRef = useRef([]);

    const handleButtonClick = (question) => {
        setActiveQuestion(question);
    };

    const handleTabClick = (tab) => {
        setActiveTab(tab);
    };

    const questions = {
        Q1: {
            question: "What do you like to do in your free time?",
            textFeedback: {
                complexity: "문장이 모두 간단하게 구성되어 있어 내용 전달이 명확했으나, 복문이나 긴 문장을 사용하면 한층 풍부한 문장의 다양성을 더할 수 있어요.",/*사용자 개인화*/
                grammarScore: "87.27 %", /*사용자 개인화*/
                grammarExample: "I like to watch a movie once a week sometimes.", /*사용자 개인화*/
                coherenceScore: "낮음"/*사용자 개인화*/
            },
            audioFeedback: {
                pronunciation: "발음이 명확하고 이해하기 쉬웠습니다.", /*사용자 개인화*/
                mlr: "10.0",/*사용자 개인화*/
                pr: "0.8"/*사용자 개인화*/
            }
        },
        Q2: {
            question: "Second question goes here",
            textFeedback: {
                complexity: "문장이 모두 간단하게 구성되어 있어 내용 전달이 명확했으나, 복문이나 긴 문장을 사용하면 한층 풍부한 문장의 다양성을 더할 수 있어요.",/*사용자 개인화*/
                grammarScore: "80.27 %", /*사용자 개인화*/
                grammarExample: "I like to watch a movie once a week sometimes.", /*사용자 개인화*/
                coherenceScore: "낮음"/*사용자 개인화*/
            },
            audioFeedback: {
                pronunciation: "발음이 명확하고 이해하기 쉬웠습니다.", /*사용자 개인화*/
                mlr: "11.0",/*사용자 개인화*/
                pr: "0.6"/*사용자 개인화*/
            }
        },
        Q3: {
            question: "Third question goes here",
            textFeedback: {
                complexity: "문장이 모두 간단하게 구성되어 있어 내용 전달이 명확했으나, 복문이나 긴 문장을 사용하면 한층 풍부한 문장의 다양성을 더할 수 있어요.",/*사용자 개인화*/
                grammarScore: "90.27 %",/*사용자 개인화*/
                grammarExample: "I like to watch a movie once a week sometimes.", /*사용자 개인화*/
                coherenceScore: "낮음"/*사용자 개인화*/
            },
            audioFeedback: {
                pronunciation: "발음이 명확하고 이해하기 쉬웠습니다.",/*사용자 개인화*/
                mlr: "12.0",/*사용자 개인화*/
                pr: "0.5"/*사용자 개인화*/
            }
        }
    };

    useEffect(() => {
        tabButtonsRef.current.forEach((button, index) => {
            if (button) {
                button.addEventListener('click', () => handleButtonClick(`Q${index + 1}`));
            }
        });

        return () => {
            tabButtonsRef.current.forEach((button, index) => { // index 추가
                if (button) {
                    button.removeEventListener('click', () => handleButtonClick(`Q${index + 1}`));
                }
            });
        };
    }, []);

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
                <div class="feedback-container">
                    <h4>You are likely to get</h4> 
                    <h1>IH</h1> 
                    <div className="tabs">
                        <button ref={el => tabButtonsRef.current[0] = el}>Q1</button>
                        <button ref={el => tabButtonsRef.current[1] = el}>Q2</button>
                        <button ref={el => tabButtonsRef.current[2] = el}>Q3</button>
                    </div>

                    <div className='feedback-box'>
                        <div className="tab-toggle">
                            <button 
                                className={activeTab === 'Text' ? 'active' : ''} 
                                onClick={() => handleTabClick('Text')}
                            >
                                Text
                            </button>
                            <button 
                                className={activeTab === 'Audio' ? 'active' : ''} 
                                onClick={() => handleTabClick('Audio')}
                            >
                                Audio
                            </button>
                        </div>

                        {activeQuestion && (
                            <h3>{questions[activeQuestion].question}</h3>
                        )}
                        {activeQuestion && activeTab === 'Text' && (
                            <div className="feedback-content">
                                <div className="feedback-row">
                                    <div className="feedback-category coherence">
                                        <h4>Coherence</h4>
                                        <p>coherence는 주제에 맞는 흐름을 유지하며 명확하게 전달되는지 확인하는 요소입니다.</p>
                                        <p className="coherence score">{questions[activeQuestion].textFeedback.coherenceScore}</p>
                                    </div>
                                    <div className="feedback-category complexity">
                                        <h4>Complexity</h4>
                                        <p>{questions[activeQuestion].textFeedback.complexity}</p>
                                    </div>
                                </div>
                                <div className="feedback-row">
                                    <div className="feedback-category grammar">
                                        <h4>Grammar</h4>
                                        <p>전체 발화 중 올바른 문법 사용 비율은</p>
                                        <p className="output score">{questions[activeQuestion].textFeedback.grammarScore}</p>
                                        <p>{questions[activeQuestion].textFeedback.grammarExample}</p>
                                    </div>
                                </div>
                            </div>
                        )}
                            
                        {activeQuestion && activeTab === 'Audio' && (
                            <div className="feedback-content">
                                <div className="feedback-row">
                                    <div className="feedback-category pronunciation">
                                        <h4>Pronunciation</h4>
                                        <p className='pronunciation score'>{questions[activeQuestion].audioFeedback.pronunciation}</p>
                                    </div>
                                    <div className="feedback-category mlr">
                                        <h4>MLR</h4>
                                        <p>사용자가 연속적으로 발음한 평균 단어 수입니다. MLR이 높을수록 보다 유창함을 보여주는 지표입니다.</p>
                                        <p className="mlr score">{questions[activeQuestion].audioFeedback.mlr}</p>
                                    </div>
                                    <div className="feedback-category pr">
                                        <h4>PR</h4>
                                        <p>사용자의 발음이 원어민과 얼마나 유사한 지 보여주는 지표입니다.</p>
                                        <p className='pr score'>{questions[activeQuestion].audioFeedback.pr}</p>
                                    </div>
                                </div>
                            </div>
                    )}
                </div>
                </div>
            </main>
        </div>
               

    );
}

export default FeedbackPage;
