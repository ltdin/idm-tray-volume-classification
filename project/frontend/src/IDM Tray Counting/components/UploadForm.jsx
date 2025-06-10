import React from 'react';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import SearchIcon from '@mui/icons-material/Search';

function UploadForm({ onRackIdImageChange, rackIdText, onImageChange, onSubmit }) {
  return (
    <div style={{ textAlign: 'center' }}>

      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="rack-id-upload"
          style={{
            padding: '0.6rem 1.2rem',
            backgroundColor: '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
          Upload Rack ID Image
          <input
            id="rack-id-upload"
            type="file"
            accept="image/*"
            style={{ display: 'none' }}
            onChange={(e) => onRackIdImageChange(e.target.files[0])}
          />
        </label>

      </div>

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
          multiple
          style={{ display: 'none' }}
          onChange={(e) => onImageChange(Array.from(e.target.files))}
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
