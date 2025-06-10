import React, { useState } from 'react';
import axios from 'axios';

function RackOCRChecker() {
  const [image, setImage] = useState(null);
  const [expectedId, setExpectedId] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
    setResult(null);
  };

  const handleSubmit = async () => {
    if (!image || !expectedId) return;

    const formData = new FormData();
    formData.append('image', image);
    formData.append('expected_id', expectedId);

    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/ocr-check', formData);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', background: '#fff', padding: '2rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
      <h3>Rack OCR Check</h3>

      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        style={{ marginTop: '1rem' }}
      />

      <input
        type="text"
        placeholder="Expected Rack ID"
        value={expectedId}
        onChange={(e) => setExpectedId(e.target.value)}
        style={{ display: 'block', marginTop: '1rem', padding: '0.5rem', width: '100%' }}
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{ marginTop: '1rem', padding: '0.6rem 1.2rem', backgroundColor: '#0068b5', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
      >
        {loading ? 'Checking...' : 'Submit'}
      </button>

      {result && (
        <div style={{ marginTop: '2rem' }}>
          <p><strong>Expected ID:</strong> {result.expected_id}</p>
          <p><strong>Extracted Text:</strong> {result.extracted_text}</p>
          <p><strong>Match:</strong> {result.match ? 'Matched' : 'Not Matched'}</p>
        </div>
      )}
    </div>
  );
}

export default RackOCRChecker;
