import React from 'react';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import AddCircleOutlineRoundedIcon from '@mui/icons-material/AddCircleOutlineRounded';
const UploadButton = ({ label, inputId, accept, multiple, onChange }) => (
  <div style={{ marginBottom: '1rem' }}>
    <label style={{
      display: 'block',
      marginBottom: '0.5rem',
      color: '#333',
      fontWeight: 'bold'
    }}>
      {label}
    </label>
    <label
      htmlFor={inputId}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '0.5rem',
        color: '#0068b5',
        padding: '0.6rem 1.2rem',
        borderRadius: '8px',
        cursor: 'pointer'
      }}
    >
      <AddCircleOutlineRoundedIcon />
      <input
        id={inputId}
        type="file"
        accept={accept}
        multiple={multiple}
        style={{ display: 'none' }}
        onChange={onChange}
      />
    </label>
  </div>
);

export default UploadButton;
