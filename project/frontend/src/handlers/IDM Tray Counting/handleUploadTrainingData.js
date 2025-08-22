import { validateUploadData } from './validateUploadData';
import { uploadTrainingDataApi } from '../../api/trainingAPI';

export const handleUploadTrainingData = async (
  yoloImages,
  yoloLabels,
  volume,
  note
) => {

  const error = validateUploadData(yoloImages, yoloLabels, volume);
  if (error) {
    alert(error);
    return;
  }

  const formData = new FormData();
  yoloImages.forEach(file => {
    formData.append('yolo_images', file);
  });
  yoloLabels.forEach(file => {
    formData.append('yolo_labels', file);
  });
  formData.append('volume', volume);
  formData.append('note', note);

  try {
    const res = await uploadTrainingDataApi(formData);
    alert(res.data.message || 'Training data uploaded!');
  } catch (err) {
    console.error(err);
    if (err.response && err.response.data?.error) {
      alert(err.response.data.error);
    } else {
      alert('Upload failed. Please try again.');
    }
  }
};
