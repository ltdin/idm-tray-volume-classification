import React, { useState } from 'react';
import FineTuneForm from '../components/FineTuneForm';
import ImagePreviewPanel from '../components/ImagePreviewPanel';
import { handleYoloImageChange } from '../handlers/handleYoloImageChange';
import { handleYoloLabelChange } from '../handlers/handleYoloLabelChange';
import { handleUploadTrainingData } from '../handlers/handleUploadTrainingData';
import { handleRetrainModels } from '../handlers/handleRetrainModels';
import ModelVersionsPanel from '../components/ModelVersionsPanel';
import LabelPreviewPanel from '../components/LabelPreviewPanel';

function IDMFineTunePage() {
  const [yoloImages, setYoloImages] = useState([]);
  const [previewUrls, setPreviewUrls] = useState([]);
  const [yoloLabels, setYoloLabels] = useState([]);
  const [volume, setVolume] = useState('');
  const [note, setNote] = useState('');
  const [progress, setProgress] = useState('');
  const [errorMessage, setErrorMessage] = useState(null);


  const onYoloImageChange = (e) => {
    handleYoloImageChange(e, setYoloImages, setPreviewUrls);
  };

  const onYoloLabelChange = (e) => {
    handleYoloLabelChange(e, setYoloLabels);
  };

  const onUploadTrainingData = () => {
    handleUploadTrainingData(
      yoloImages,
      yoloLabels,
      volume,
      note,
      setProgress,
      setErrorMessage
    );
  };

  const onRetrain = () => {
    handleRetrainModels(setProgress);
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '2rem',
      padding: '2rem'
    }}>
      <div style={{
        display: 'flex',
        gap: '2rem',
        alignItems: 'flex-start'
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
        <LabelPreviewPanel
          yoloLabels={yoloLabels}
        />
      </div>

      <div style={{ width: '100%' }}>
        <ModelVersionsPanel />
      </div>
      {errorMessage && (
        <div style={{
          background: '#f8d7da',
          color: '#721c24',
          border: '1px solid #f5c6cb',
          padding: '1rem',
          borderRadius: '4px',
          marginTop: '1rem'
        }}>
          <strong>Error:</strong> {errorMessage}
        </div>
      )}

    </div>
  );
}

export default IDMFineTunePage;
