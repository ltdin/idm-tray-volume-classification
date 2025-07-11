import axios from 'axios';

export const fetchVersions = async () => {
  const res = await axios.get('http://localhost:5001/api/model/versions');
  return res.data;
};

export const switchVersion = async (version_name) => {
  const res = await axios.post('http://localhost:5001/api/model/use-version', {
    version_name,
  });
  return res.data;
};

export const deleteVersion = async (version_name) => {
  const res = await axios.post('http://localhost:5001/api/model/delete-version', {
    version_name,
  });
  return res.data;
};
