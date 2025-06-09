import React from 'react';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import SearchIcon from '@mui/icons-material/Search';

function UploadForm({ onImageChange, onSubmit }) {
  return (
    <div style={{ textAlign: 'center' }}>
      <label htmlFor="file-upload"
        style={{
          marginLeft: '1rem',
          padding: '0.6rem 1.2rem',
          backgroundColor: '#0068b5',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
        <CloudUploadIcon />
        <input
          id="file-upload"
          type="file"
          accept="image/*"
          style={{ display: 'none' }}
          onChange={(e) => onImageChange(e.target.files[0])}
        />
      </label>

      <button
        onClick={onSubmit}
        style={{
          marginLeft: '1rem',
          padding: '0.6rem 1.2rem',
          backgroundColor: '#0068b5',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}
      >
        <SearchIcon />
      </button>
    </div>
  );
}

export default UploadForm;
