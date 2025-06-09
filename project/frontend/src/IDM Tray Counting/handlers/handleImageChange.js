const handleImageChange = (file, setImage, setPreview, setResult) => {
  setImage(file);
  setPreview(URL.createObjectURL(file));
  setResult(null);
};

export default handleImageChange;


