import axios from 'axios';

const handleSubmit = async (images, setResult, rackIdText) => {
  if (!images || images.length === 0) return;

  const formData = new FormData();
  images.forEach(file => formData.append('images', file));
  formData.append('rack_id', rackIdText || 'rack');

  try {
    const res = await axios.post("http://localhost:5000/predict", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    setResult(res.data.results || []);
  } catch (error) {
    console.error("Prediction failed:", error);
    setResult([]);
  }
};

export default handleSubmit;
