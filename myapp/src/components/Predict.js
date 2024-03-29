import React, { useState, useEffect } from 'react';

const PredictOutcome = ({ runs, wickets, overs, balls, firstInnings, chasingScore , predictCounter}) => {
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
  
    setPrediction(null);
    setError(null);
    predictOutcome(); 
  }, [predictCounter]);

  const predictOutcome = () => {
    const apiUrl = 'http://0.0.0.0:8000/predict/';

    const oversWithBalls = parseFloat(overs) + parseFloat(balls) / 6; 
    const data = {
      runs: parseInt(runs),
      wickets: parseInt(wickets),
      overs: parseFloat(oversWithBalls),
      second_innings: firstInnings,
      chasing_score: firstInnings ? -1 : parseInt(chasingScore),
    };

    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => setPrediction(data))
    .catch(error => setError(error));
  };


    return (
    <div className="flex items-center justify-center h-screen bg-grass-pattern"> 
      {prediction && (
        <div className="max-w-lg mx-auto p-6 rounded-lg shadow-lg bg-white border-2 border-green-600"> 
          <h2 className="text-center font-bold text-xl uppercase text-green-700 mb-4">Prediction Outcome</h2>
          <ul className="list-decimal list-inside">
            {Object.entries(prediction).map(([key, value]) => (
              <li key={key} className="font-medium text-gray-700 mb-1">
                <strong>{key.replace(/_/g, ' ').toUpperCase()}:</strong> {typeof value === 'number' ? value.toFixed(2) : value.toString().toUpperCase()} 
              </li>
            ))}
          </ul>
        </div>
      )}
      {error && (
      <div className="max-w-lg mx-auto p-6 mt-4 rounded-lg shadow-lg bg-white border-2 border-red-600"> 
        <p className="text-center text-lg font-semibold uppercase text-red-700">{error.message}</p> 
      </div>
    )}
  </div>
  );
   
};

export default PredictOutcome;
