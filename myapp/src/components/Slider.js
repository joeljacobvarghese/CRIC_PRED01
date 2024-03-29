import * as React from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import Typography from '@mui/material/Typography'; // Import Typography for the label

export default function ChasingScoreInput({ value, onChange, min, max, label }) {
  return (
    <Box sx={{ width: 400, display: 'flex', alignItems: 'center' }}> {/* Use flex layout */}
      
      <Slider
        value={value || 0} // Ensure we have a number even if value is null
        min={min}
        step={1}
        max={max} // Set the max value
        aria-label={label}
        valueLabelDisplay="auto"
        onChange={(e, newValue) => onChange(newValue)}
        sx={{ flexGrow: 1 }} // Allow the slider to fill the rest of the box's space
      />
    </Box>
  );
}
