import React from 'react';
import UploadForm from '../components/UploadForm';
import ImagePreview from '../components/ImagePreview';
import AnnotatedResult from '../components/AnnotatedResult';
import ResultTable from '../components/ResultTable';
import handleImageChange from '../handlers/handleImageChange';
import handleSubmit from '../handlers/handleSubmit';
import handleRackIdImageChange from '../handlers/handleRackIdImageChange';

function TrayCounting({
  images,
  setImages,
  previews,
  setPreviews,
  results,
  setResults,
  rackIdImage,
  setRackIdImage,
  rackIdText,
  setRackIdText,
}) {
  const groupedResults = {};
  results.forEach((res) => {
    const groupId = res.racks[0]?.rack_id.split('No.')[0];
    if (!groupedResults[groupId]) {
      groupedResults[groupId] = [];
    }
    groupedResults[groupId].push(res);
  });

  return (
    <div style={{ padding: '2rem' }}>
      <div
        style={{
          background: '#fff',
          padding: '2rem',
          borderRadius: '12px',
          marginBottom: '2rem',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        }}
      >
        <UploadForm
  onRackIdImageChange={(file) =>
    handleRackIdImageChange(file, setRackIdImage, setRackIdText)
  }
  rackIdText={rackIdText}
  rackIdImage={rackIdImage}
  onImageChange={(files) =>
    handleImageChange(files, setImages, setPreviews, setResults)
  }
  onSubmit={() =>
    handleSubmit(images, setResults, rackIdText)
  }
/>

        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '1rem',
            justifyContent: 'center',
            marginTop: '1rem',
          }}
        >
          {Array.isArray(previews) &&
            previews.map((src, index) => (
              <ImagePreview key={index} src={src} />
            ))}
        </div>
      </div>

      {Object.keys(groupedResults).length > 0 && (
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '2rem',
          }}
        >
          {Object.entries(groupedResults).map(([groupId, groupItems]) => (
            <div
              key={groupId}
              style={{
                background: '#fff',
                padding: '2rem',
                borderRadius: '12px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                marginBottom: '2rem',
              }}
            >
              <h4 style={{ marginBottom: '1rem' }}>
                Rack ID Group: {groupId}
              </h4>

              <div
                style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  gap: '2rem',
                  justifyContent: 'center',
                }}
              >
                {groupItems.map((res, idx) => (
                  <div
                    key={idx}
                    style={{ flex: '1 1 45%' }}
                  >
                    <AnnotatedResult imageUrl={res.annotated_path} />
                  </div>
                ))}
              </div>

              <div style={{ marginTop: '1rem' }}>
                <ResultTable
                  data={groupItems.flatMap((res) => res.racks)}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default TrayCounting;
