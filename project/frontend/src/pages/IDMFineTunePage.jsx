import React, { useState } from 'react';
import FineTuneForm from '../components/FineTuneForm'; 
import ImagePreviewPanel from '../components/ImagePreviewPanel';
import { handleYoloImageChange } from '../handlers/handleYoloImageChange';
import { handleYoloLabelChange } from '../handlers/handleYoloLabelChange';
import { handleUploadTrainingData } from '../handlers/handleUploadTrainingData';
import { handleRetrainModels } from '../handlers/handleRetrainModels';

function IDMFineTunePage() {
  const [yoloImages, setYoloImages] = useState([]);
  const [previewUrls, setPreviewUrls] = useState([]);
  const [yoloLabels, setYoloLabels] = useState([]);
  const [volume, setVolume] = useState('');
  const [note, setNote] = useState('');
  const [progress, setProgress] = useState('');

  // Wrap handlers with local state
  const onYoloImageChange = (e) => {
    handleYoloImageChange(e, setYoloImages, setPreviewUrls);
  };

  const onYoloLabelChange = (e) => {
    handleYoloLabelChange(e, setYoloLabels);
  };

  const onUploadTrainingData = () => {
    handleUploadTrainingData(yoloImages, yoloLabels, volume, note);
  };

  const onRetrain = () => {
    handleRetrainModels(setProgress);
  };

  return (
    <div style={{
      display: 'flex',
      gap: '2rem',
      alignItems: 'flex-start',
      padding: '2rem'
    }}>
      <FineTuneForm
        yoloImages={yoloImages}
        yoloLabels={yoloLabels}
        volume={volume}
        note={note}
        setVolume={setVolume}
        setNote={setNote}
        handleYoloImageChange={onYoloImageChange}
        handleYoloLabelChange={onYoloLabelChange}
        handleUploadTrainingData={onUploadTrainingData}
        handleRetrain={onRetrain}
        progress={progress}
      />

      <ImagePreviewPanel
        previewUrls={previewUrls}
        yoloImages={yoloImages}
      />
    </div>
  );
}

export default IDMFineTunePage;
