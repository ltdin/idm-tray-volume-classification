import axios from 'axios';

const handleRackIdImageChange = async (file, setRackIdImage, setRackIdText) => {
  setRackIdImage(file);

  const formData = new FormData();
  formData.append("image", file);
  formData.append("expected_id", ""); 

  try {
    const res = await axios.post("http://localhost:5000/ocr-check", formData);
    if (res.data.extracted_text) {
      setRackIdText(res.data.extracted_text);
    } else {
      setRackIdText('UNKNOWN');
    }
  } catch {
    setRackIdText('ERROR');
  }
};

export default handleRackIdImageChange;
