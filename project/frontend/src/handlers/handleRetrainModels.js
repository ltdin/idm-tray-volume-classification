import { retrainModelsApi } from "../api/trainingAPI";
export const handleRetrainModels = async (setProgress) => {
  try {
    setProgress('Retrain in progress...');
    const res = await retrainModelsApi();
    setProgress(res.data.message);
  } catch (error) {
    console.error(error);
    setProgress('Retrain failed.');
  }
};
