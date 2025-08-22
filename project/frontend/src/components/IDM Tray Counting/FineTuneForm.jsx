import React from 'react';
import UploadButton from './UploadButton';
import LinearProgress from '@mui/material/LinearProgress';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutline';
import Tooltip from '@mui/material/Tooltip';

const FineTuneForm = ({
  yoloImages,
  yoloLabels,
  volume,
  note,
  setVolume,
  setNote,
  handleYoloImageChange,
  handleYoloLabelChange,
  handleUploadTrainingData,
  handleRetrain,
  progress
}) => (
  <div style={{ flex: '2' }}>
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        marginBottom: '1rem'
      }}
    >
      <h2 style={{ color: '#0068b5', margin: 0 }}>Fine-Tune Models (Tray Counting)</h2>
      <Tooltip
        title={
          <span style={{ fontSize: '1rem' }}>
            1. Click Add button at Upload YOLO Images to upload data images for fine-tune.<br />
            2. Click Add button at Upload YOLO Label Files (.txt) to upload label files for fine-tune.<br />
            3. Choose volume label percentage.<br />  
            4. Field Note is optional, you can add any note for this fine-tune.<br />
            5. Click Upload Training Data button to upload training data to server.<br /> 
            6. Click Start Retrain button to start retraining the model with uploaded data.<br />
            7. Retraining progress will be shown below.<br />
            8. You can view all Model Versions in Model Versions panel and select one.
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
        htmlFor="yolo-image-upload"
        style={{
          minWidth: '150px',
          color: '#333',
          fontWeight: 'bold'
        }}
      >
        Upload YOLO Images
      </label>

      <UploadButton
        label=""
        inputId="yolo-image-upload"
        accept="image/*"
        multiple
        onChange={handleYoloImageChange}
        small
      />
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
        htmlFor="yolo-label-upload"
        style={{
          minWidth: '150px',
          color: '#333',
          fontWeight: 'bold'
        }}
      >
        Upload YOLO Label Files (.txt)
      </label>

      <UploadButton
        label=""
        inputId="yolo-label-upload"
        accept=".txt"
        multiple
        onChange={handleYoloLabelChange}
        small
      />
    </div>

    <div style={{ marginBottom: '1rem' }}>
      <label>Volume Label (%)</label><br />
      <select
        value={volume}
        onChange={(e) => setVolume(e.target.value)}
        style={{
          width: '200px',
          padding: '0.5rem',
          borderRadius: '4px',
          border: '1px solid #ccc'
        }}
      >
        <option value="">Select Volume %</option>
        {[0, 20, 40, 60, 80, 100].map((v) => (
          <option key={v} value={v}>
            {v}%
          </option>
        ))}
      </select>
    </div>

    <div style={{ marginBottom: '1rem' }}>
      <label>Note</label><br />
      <textarea
        rows="2"
        value={note}
        onChange={(e) => setNote(e.target.value)}
        style={{
          width: '100%',
          padding: '0.5rem',
          borderRadius: '4px',
          border: '1px solid #ccc'
        }}
      ></textarea>
    </div>

    <div style={{ marginBottom: '1rem' }}>
      <button
        onClick={handleUploadTrainingData}
        style={{
          padding: '0.6rem 1.2rem',
          backgroundColor: '#28a745',
          color: '#fff',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          marginRight: '1rem'
        }}
      >
        Upload Training Data
      </button>

      <button
        onClick={handleRetrain}
        style={{
          padding: '0.6rem 1.2rem',
          backgroundColor: '#0068b5',
          color: '#fff',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        Start Retrain
      </button>
    </div>

    {progress === 'Retrain in progress...' ? (
      <div style={{ width: '100%', marginTop: '1rem' }}>
        <LinearProgress color="primary" />
      </div>
    ) : progress && (
      <div style={{ marginTop: '2rem', color: '#0068b5' }}>
        <strong>{progress}</strong>
      </div>
    )}
  </div>
);

export default FineTuneForm;
