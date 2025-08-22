import { generatePreviewUrls } from './generatePreviewUrls';

export const handleYoloImageChange = (e, setYoloImages, setPreviewUrls) => {
  const files = Array.from(e.target.files);
  setYoloImages(files);
  const urls = generatePreviewUrls(files);
  setPreviewUrls(urls);
};
