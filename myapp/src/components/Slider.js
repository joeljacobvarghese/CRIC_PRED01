import * as React from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';


export default function ChasingScoreInput({ value, onChange, min, max, label }) {
  return (
    <Box sx={{ width: 400, display: 'flex', alignItems: 'center' }}> 
      
      <Slider
        value={value || 0} 
        min={min}
        step={1}
        max={max} 
        aria-label={label}
        valueLabelDisplay="auto"
        onChange={(e, newValue) => onChange(newValue)}
        sx={{ flexGrow: 1 }} 
      />
    </Box>
  );
}
