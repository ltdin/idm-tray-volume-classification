import axios from 'axios';

export const sendPredictRequest = async (imageFile) => {
  const formData = new FormData();
  formData.append("images", imageFile);

  const response = await axios.post("http://localhost:5000/predict", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  return response.data;
};