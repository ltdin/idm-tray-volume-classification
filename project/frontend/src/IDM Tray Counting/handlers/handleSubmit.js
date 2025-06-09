import { sendPredictRequest } from '../api/predict';

const handleSubmit = async (image, setResult) => {
  if (!image) return;
  const res = await sendPredictRequest(image);
  
  // Check if the response contains results
  if (res.results && res.results.length > 0) {
    setResult(res.results[0]);
  } else {
    setResult(null);
  }
};

export default handleSubmit;
