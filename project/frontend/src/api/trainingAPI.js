import axios from 'axios';

export const uploadTrainingDataApi = (formData) => {
  return axios.post('http://localhost:5000/api/training/upload', formData);
};

export const retrainModelsApi = () => {
  return axios.post('http://localhost:5000/api/training/retrain');
};
