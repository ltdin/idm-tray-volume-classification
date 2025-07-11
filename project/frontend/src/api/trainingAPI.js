import axios from 'axios';

export const uploadTrainingDataApi = (formData) => {
  return axios.post('http://localhost:5001/api/training/upload', formData);
};

export const retrainModelsApi = () => {
  return axios.post('http://localhost:5001/api/training/retrain');
};
