import React from 'react';

function AnnotatedResult({ imageUrl }) {
  if (!imageUrl) return null;

  return (
    <div style={{ marginTop: '1rem' }}>
      <h4>Annotated Result:</h4>
      <img src={imageUrl} alt="Result" width={600} />
    </div>
  );
}

export default AnnotatedResult;
