import React from 'react';

const FeedbackPage = () => {
  const { user, date } = useContext(UserContext);
  const [data, setData] = useState(null);

  const getTotalScore = async (date) => {
    try {
      const response = await fetch(`http://localhost:8000/api/me/result/${date}`, {
        method: 'GET',
        headetrs: {
          'Content-Type': 'application/json',
        }
      });
      if (response.ok) {
        const score = await response.json();
        console.log(data);
        setData(score);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  useEffect(() => {
    getTotalScore(date);
  }, [date]);

  const getResult = async (date, q_num) => {
    try {
      const response = await fetch(`http://localhost:8000/api/me/result/${date}/${q_num}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.ok) {
        const data = await response.json();
        console.log(data);
        setData(data);
      } else {
        console.error('no data');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleButtonClick = (q_num) => {
    getQuestion(date);
    getResult(date, q_num);
  };

  return (
    <div>
      <h1>피드백 페이지</h1>
      <div>
        {score ? (
          <p>총합: {score.score}</p>
        ) : (
          <p>데이터가 없습니다.</p>
        )}
      </div>
      <div className="button-container">
        <button className="q1" onClick={() => handleButtonClick(1)}>1</button>
        <button className="q2" onClick={() => handleButtonClick(2)}>2</button>
        <button className="q3" onClick={() => handleButtonClick(3)}>3</button>
      </div>
      <div>
        {question ? (
          <p><strong>question:</strong> {question.q1}</p>
        ): (
          <p>데이터가 없습니다</p>
        )}
      </div>
      <div>
        {data ? (
          <div>
            <p><strong>mpr:</strong> {data.mpr}</p>
            <p><strong>coherence:</strong> {data.coherence}</p>
            <p><strong>complexity:</strong> {data.complexity}</p>
            <p><strong>grammar:</strong> {data.grammar}</p>
            <p><strong>wpm:</strong> {data.wpm}</p>
            <p><strong>pause:</strong> {data.pause}</p>
            <p><strong>mlr:</strong> {data.mlr}</p>
          </div>
        ) : (
          <p>데이터가 없습니다</p>
        )}
      </div>
    </div>
  );
};

export default FeedbackPage;