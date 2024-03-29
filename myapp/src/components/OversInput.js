import React, { useState, useEffect } from 'react';
import { InputNumber, Form } from 'rsuite';

function CricketOversInput({ initialOvers = 0, maxOvers = 0, onChange, balls, overs, setOvers, setBalls }) {

  useEffect(() => {
    if (balls > 6) {
      if(overs < maxOvers)
      setOvers(prevOvers => prevOvers + Math.floor(balls / 7));
      setBalls(0);
    }
  }, [balls, setOvers, setBalls]);

  // Call the onChange prop whenever overs or balls change
  useEffect(() => {
    if (onChange) {
      onChange({ overs, balls });
    }
  }, [overs, balls, onChange]);

  // Handle changes in balls
  const handleBallsChange = (value) => {
    setBalls(Number(value));
  };

  // Handle changes in overs
  const handleOversChange = (value) => {
    setOvers(Number(value));
  };

  return (
    <Form fluid>
      <div style={{ display: 'flex', gap: '0' }}>
        <InputNumber
          min={0}
          max={maxOvers}
          value={overs}
          onChange={handleOversChange}
          style={{ flex: 1 }}
        />
        <InputNumber
          min={0}
          max={7}
          value={balls}
          onChange={handleBallsChange}
          style={{ flex: 1 }}
        />
      </div>
    </Form>
  );
}

export default CricketOversInput;
