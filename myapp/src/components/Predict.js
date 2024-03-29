import React, { useState, useEffect } from 'react';

const PredictOutcome = ({ runs, wickets, overs, balls, firstInnings, chasingScore , predictCounter}) => {
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Reset the prediction and error state before making a new prediction
    setPrediction(null);
    setError(null);
    predictOutcome(); // Call predictOutcome when the component props change
  }, [predictCounter]);

  const predictOutcome = () => {
    const apiUrl = 'http://0.0.0.0:8000/predict/';

    const oversWithBalls = parseFloat(overs) + parseFloat(balls) / 6; // Assuming 6 balls per over
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

  // ... (rest of your PredictOutcome component)

    return (
    <div className="flex items-center justify-center h-screen bg-grass-pattern"> {/* Replace 'bg-grass-pattern' with your actual grass background */}
      {prediction && (
        <div className="max-w-lg mx-auto p-6 rounded-lg shadow-lg bg-white border-2 border-green-600"> {/* Box styling with border for definition */}
          <h2 className="text-center font-bold text-xl uppercase text-green-700 mb-4">Prediction Outcome</h2>
          <ul className="list-decimal list-inside">
            {Object.entries(prediction).map(([key, value]) => (
              <li key={key} className="font-medium text-gray-700 mb-1">
                <strong>{key.replace(/_/g, ' ').toUpperCase()}:</strong> {typeof value === 'number' ? value.toFixed(2) : value.toString().toUpperCase()} {/* Key uppercase, number formatting or uppercase for string values */}
              </li>
            ))}
          </ul>
        </div>
      )}
      {error && (
      <div className="max-w-lg mx-auto p-6 mt-4 rounded-lg shadow-lg bg-white border-2 border-red-600"> {/* Error message box styling with red border for emphasis */}
        <p className="text-center text-lg font-semibold uppercase text-red-700">{error.message}</p> {/* Error message styling with uppercase and red color */}
      </div>
    )}
  </div>
  );
   
};

export default PredictOutcome;
