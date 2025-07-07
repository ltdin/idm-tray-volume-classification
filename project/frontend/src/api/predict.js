import axios from 'axios';

export const sendPredictRequest = async (imageFiles) => {
  const formData = new FormData();
  imageFiles.forEach(file => formData.append("images", file));

  const response = await axios.post("http://localhost:5000/predict", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  return response.data;
};
