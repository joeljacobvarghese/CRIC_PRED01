import React, { useState } from 'react';
import OversInput from './components/OversInput';
import Slider from './components/Slider.js';
import CheckBox from './components/CheckBox';
import PredictOutcome from './components/Predict.js';
import { MdSportsCricket } from 'react-icons/md'; // Importing a cricket icon for the button



function App() {
  
  const [runs, setRuns] = useState(0);
  const [wickets, setWickets] = useState(0);
  const [overs, setOvers] = useState(0);
  const [balls, setBalls] = useState(0); 
  const [chasingScore, setChasingScore] = useState(0);
  const [firstInnings, setFirstInnings] = useState(false);
  const [predictCounter, setPredictCounter] = useState(0);
  

  const handleFirstInningsChange = (event) => {
    setFirstInnings(event.target.checked);
    if (!event.target.checked) {
      setChasingScore(-1);
    }
  };

  const handleClick = () => {
    setPredictCounter(prevCount => prevCount + 1);
  };
  

  
  return (
    <div className="relative min-h-screen bg-gray-100">
      <div
        className="bg-cover bg-center w-full"
        style={{
          backgroundImage: 'url(/field.jpeg)',
          height: '60vh'
        }}
      >
        <div className="flex flex-col items-center justify-center h-full relative">
          <div className="rounded-full bg-red-600 p-10 text-white shadow-lg hover:shadow-2xl transition">
            <MdSportsCricket size="4em" />
          </div>  
          <button
            variant="contained"
            color="primary"
            onClick={handleClick}
            className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transform transition hover:scale-105 duration-300 ease-in-out"
          >
            Predict
          </button>
          {predictCounter >0 && (
              <PredictOutcome
                key={predictCounter}
                overs={overs}
                balls={balls}
                runs={runs}
                wickets={wickets}
                firstInnings={firstInnings}
                chasingScore={chasingScore}
              />
          )}
        </div>
      </div>

      <div className="flex-1 px-3 py-8">
        <div className="w-full max-w-7xl mx-auto bg-white rounded-xl shadow-lg p-6 min-h-28">
          <CheckBox
            checked={firstInnings}
            onChange={handleFirstInningsChange}
            label={<span className="text-lg">SECOND INNINGS</span>} 
            className="w-full mb-6"
          />
          <div className="mb-4 grid grid-cols-3 gap-4 items-center text-lg">
            <label className="block text-left col-span-1 text-lg">RUNS:</label>
            <Slider value={runs} onChange={setRuns} min = {0} max = {500} label = {"RUNS"} className="col-span-2" />
            <span>{runs}</span>
          </div>
          <div className="mb-4 grid grid-cols-3 gap-4 items-center text-lg">
            <label className="block text-left col-span-1 text-lg">WICKETS:</label>
            <Slider value={wickets} onChange={setWickets} min = {0} max = {10} label = {"WICKETS"} className="col-span-2" />
            <span>{wickets}</span>
          </div>
          <div className="mb-4 grid grid-cols-3 gap-4 items-center text-lg">
            <label className="block text-left col-span-1 text-lg">OVERS:</label>
            <OversInput maxOvers = {50} balls = {balls} overs = {overs} setOvers = {setOvers} setBalls={setBalls} className="col-span-2" />
          </div>
          {firstInnings && (
            <div className="grid grid-cols-3 gap-4 items-center text-lg">
              <label className="block text-left col-span-1 text-lg">CHASING SCORE:</label>
              <Slider value={chasingScore} onChange={setChasingScore} min = {0} max = {500} label = {"CHASING SCORE"} className="col-span-2" />
              <span>{chasingScore}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
