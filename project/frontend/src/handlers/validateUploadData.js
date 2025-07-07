export const validateUploadData = (yoloImages, yoloLabels, volume) => {
  if (yoloImages.length === 0 || yoloLabels.length === 0 || !volume) {
    return 'Please select YOLO images, YOLO labels and volume.';
  }

  if (yoloImages.length !== yoloLabels.length) {
    return `Number of images (${yoloImages.length}) and labels (${yoloLabels.length}) do not match!`;
  }

  const imageNames = yoloImages.map(f => f.name.split('.')[0]);
  const labelNames = yoloLabels.map(f => f.name.split('.')[0]);

  const missingLabels = imageNames.filter(name => !labelNames.includes(name));
  if (missingLabels.length > 0) {
    return `Missing label files for images: ${missingLabels.join(', ')}`;
  }

  return null;
};
