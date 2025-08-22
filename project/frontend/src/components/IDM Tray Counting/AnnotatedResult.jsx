import React from 'react';

function AnnotatedResult({ imageUrl }) {
  if (!imageUrl) return null;

  return (
    <div style={{ marginTop: '1rem' }}>
      <img
        src={imageUrl}
        alt="Result"
        style={{
          width: '100%',
          height: 'auto',
          objectFit: 'cover',
          borderRadius: '8px',
          border: '1px solid #ccc',
          display: 'block'
        }}
      />
    </div>
  );
}

export default AnnotatedResult;
