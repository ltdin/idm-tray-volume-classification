import React from 'react';

const ImagePreviewPanel = ({ previewUrls, yoloImages }) => (
  <div style={{
    flex: '1',
  }}>
    <h3 style={{ color: '#0068b5' }}>Image Preview</h3>
    {previewUrls.length === 0 && (
      <p style={{ fontSize: '0.9rem', color: '#777' }}>
        No images selected.
      </p>
    )}
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 140px))',
        gap: '1rem',
        justifyContent: 'flex-start'
      }}
    >
      {previewUrls.map((url, idx) => (
        <div key={idx}>
          <img
            src={url}
            alt={`Preview ${idx}`}
            style={{
              width: '100%',
              height: '100px',
              borderRadius: '8px',
              border: '1px solid #ccc',
              objectFit: 'cover',
              display: 'block'
            }}
          />
          <p style={{
            fontSize: '0.75rem',
            wordBreak: 'break-all',
            marginTop: '0.3rem'
          }}>
            {yoloImages[idx]?.name}
          </p>
        </div>
      ))}
    </div>
  </div>
);

export default ImagePreviewPanel;
