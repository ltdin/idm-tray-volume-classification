import React from 'react';

const LabelPreviewPanel = ({ yoloLabels }) => (
  <div style={{
    flex: '1',
    maxWidth: '400px',
    borderLeft: '2px solid #e0e0e0',
    paddingLeft: '2rem'
  }}>
    <h3 style={{ color: '#0068b5' }}>Label Preview</h3>
    {yoloLabels.length === 0 && (
      <p style={{ fontSize: '0.9rem', color: '#777' }}>No label files selected.</p>
    )}

    <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
      {yoloLabels.map((file, idx) => (
        <li key={idx} style={{
          background: '#f5f5f5',
          padding: '0.5rem',
          borderRadius: '4px',
          marginBottom: '0.5rem',
          fontSize: '0.85rem',
          wordBreak: 'break-all'
        }}>
          {file.name}
        </li>
      ))}
    </ul>
  </div>
);

export default LabelPreviewPanel;
