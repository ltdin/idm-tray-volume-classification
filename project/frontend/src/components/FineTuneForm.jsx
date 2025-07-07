import React from 'react';
import UploadButton from './UploadButton';

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
    <h2 style={{ color: '#0068b5' }}>Fine-Tune Models</h2>

    <UploadButton
      label="Upload YOLO Images"
      inputId="yolo-image-upload"
      accept="image/*"
      multiple
      onChange={handleYoloImageChange}
    />

    <UploadButton
      label="Upload YOLO Label Files (.txt)"
      inputId="yolo-label-upload"
      accept=".txt"
      multiple
      onChange={handleYoloLabelChange}
    />

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
        {[0, 20, 40, 60, 80, 100].map(v => (
          <option key={v} value={v}>{v}%</option>
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

    {progress && (
      <div style={{ marginTop: '1rem', color: '#0068b5' }}>
        <strong>{progress}</strong>
      </div>
    )}
  </div>
);

export default FineTuneForm;
