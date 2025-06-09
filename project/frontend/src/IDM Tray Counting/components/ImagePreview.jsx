import React from 'react';

function ImagePreview({ src }) {
  return (
    <div style={{ marginBottom: '1rem' }}>
      <h4>Image Preview:</h4>
      <img src={src} alt="Preview" width={300} />
    </div>
  );
}

export default ImagePreview;