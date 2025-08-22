const handleImageChange = (files, setImages, setPreviews, setResult) => {
  if (!Array.isArray(files)) return;

  const previews = files.map(file => URL.createObjectURL(file));
  setImages(files);
  setPreviews(previews);
  setResult([]);
};

export default handleImageChange;
