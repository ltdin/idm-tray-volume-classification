import axios from 'axios';

const handleKanbanSubmit = async (images, setResult) => {
  if (!images || images.length === 0) return;

  const formData = new FormData();
  images.forEach((file) => formData.append('images', file));

  try {
    const res = await axios.post('http://localhost:5002/predict', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    setResult(res.data?.results || []);
  } catch (err) {
    console.error('Kanban prediction failed:', err);
    setResult([]);
  }
};

export default handleKanbanSubmit;
