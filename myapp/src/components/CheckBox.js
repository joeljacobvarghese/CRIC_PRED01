// src/components/CheckBox.js
import * as React from 'react';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';

export default function SizeCheckboxes({ checked, onChange, label }) {
  return (
    <div>
      <FormControlLabel
        control={
          <Checkbox
            checked={checked}
            onChange={onChange}
            size="small"
            inputProps={{ 'aria-label': label }}
          />
        }
        label={label}
      />
    </div>
  );
}
