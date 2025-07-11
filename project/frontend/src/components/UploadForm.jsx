import React from 'react';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import SearchIcon from '@mui/icons-material/Search';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import Tooltip from '@mui/material/Tooltip';
import AddCircleOutlineRoundedIcon from '@mui/icons-material/AddCircleOutlineRounded';

function UploadForm({
  onRackIdImageChange,
  onImageChange,
  onSubmit
}) {
  return (
    <div style={{ flex: '2' }}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          marginBottom: '1rem'
        }}
      >
        <h2 style={{ color: '#0068b5', margin: 0 }}>Tray Counting</h2>
        <Tooltip
          title={
            <span style={{ fontSize: '1rem' }}>
              1. Click Upload Rack ID Image to upload a single rack ID image.<br />
              2. Click Upload Rack Images to upload one or more rack images.<br />
              3. Click Checking to start prediction.
            </span>
          }
          placement="right"
          arrow
        >
          <InfoOutlinedIcon style={{ color: '#0068b5', cursor: 'pointer' }} />
        </Tooltip>
      </div>

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          marginBottom: '1rem',
          gap: '1rem'
        }}
      >
        <label
          htmlFor="rack-id-upload"
          style={{
            minWidth: '180px',
            color: '#333',
            fontWeight: 'bold'
          }}
        >
          Upload Rack ID Image
        </label>

        <label htmlFor="rack-id-upload"
          style={{
            padding: '0.6rem 1.2rem',
            color: '#0068b5',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
          <AddCircleOutlineRoundedIcon />
          <input
            id="rack-id-upload"
            type="file"
            accept="image/*"
            style={{ display: 'none' }}
            onChange={(e) => onRackIdImageChange(e.target.files[0])}
          />
        </label>
      </div>

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          marginBottom: '1rem',
          gap: '1rem'
        }}
      >
        <label
          htmlFor="rack-images-upload"
          style={{
            minWidth: '180px',
            color: '#333',
            fontWeight: 'bold'
          }}
        >
          Upload Rack Images
        </label>

        <label htmlFor="rack-images-upload"
          style={{
            padding: '0.6rem 1.2rem',
            color: '#0068b5',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
          <AddCircleOutlineRoundedIcon />
          <input
            id="rack-images-upload"
            type="file"
            accept="image/*"
            multiple
            style={{ display: 'none' }}
            onChange={(e) => onImageChange(Array.from(e.target.files))}
          />
        </label>
      </div>

      {/* Checking Button */}
      <div style={{ marginTop: '1rem' }}>
        <button
          onClick={onSubmit}
          style={{
            padding: '0.6rem 1.2rem',
            backgroundColor: '#0068b5',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}
        >
          Checking
        </button>
      </div>
    </div>
  );
}

export default UploadForm;
