export const generatePreviewUrls = (files) => {
  return files.map(file => URL.createObjectURL(file));
};
