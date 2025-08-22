import React from 'react';
import UploadForm from '../components/IDM Tray Counting/UploadForm';
import AnnotatedResult from '../components/IDM Tray Counting/AnnotatedResult';
import ResultTable from '../components/IDM Tray Counting/ResultTable';
import ImagePreviewPanel from '../components/IDM Tray Counting/ImagePreviewPanel';
import handleImageChange from '../handlers/IDM Tray Counting/handleImageChange';
import handleSubmit from '../handlers/IDM Tray Counting/handleSubmit';
import handleRackIdImageChange from '../handlers/IDM Tray Counting/handleRackIdImageChange';

const RackIdPanel = ({ rackIdImage, rackIdText }) => {
  return (
    <div style={{
      flex: 1,
      borderLeft: '2px solid #e0e0e0',
      paddingLeft: '2rem'
    }}>
      <h3 style={{ color: '#0068b5' }}>Rack ID Image</h3>
      {rackIdImage ? (
        <>
          <img
            src={URL.createObjectURL(rackIdImage)}
            alt="Rack ID"
            style={{
              width: '100%',
              height: 'auto',
              borderRadius: '8px',
              border: '1px solid #ccc'
            }}
          />
          {rackIdText && (
            <p style={{
              fontSize: '0.85rem',
              marginTop: '0.5rem',
              color: '#555'
            }}>
              {rackIdText}
            </p>
          )}
        </>
      ) : (
        <p style={{ color: '#777', fontSize: '0.9rem' }}>
          No Rack ID image selected.
        </p>
      )}
    </div>
  );
};

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
        <div style={{
          display: 'flex',
          gap: '2rem',
          alignItems: 'flex-start'
        }}>
          <div style={{ flex: 1 }}>
            <UploadForm
              onRackIdImageChange={(file) =>
                handleRackIdImageChange(file, setRackIdImage, setRackIdText)
              }
              onImageChange={(files) =>
                handleImageChange(files, setImages, setPreviews, setResults)
              }
              onSubmit={() =>
                handleSubmit(images, setResults, rackIdText)
              }
            />
          </div>

          <RackIdPanel rackIdImage={rackIdImage} rackIdText={rackIdText} />

          <div style={{
            flex: 2,
            paddingLeft: '2rem'
          }}>
            <ImagePreviewPanel previewUrls={previews} yoloImages={images} />
          </div>
          
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
              <div style={{ marginTop: '1rem' }}>
                <ResultTable
                  data={groupItems.flatMap((res) => res.racks)}
                />
              </div>
               <h3 style={{ color: '#0068b5' }}>
                Rack ID Group: {groupId}
              </h3>

              <div
  style={{
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
    gap: '1rem',
    justifyContent: 'flex-start'
  }}
>
  
  {groupItems.map((res, idx) => (
    <div key={idx}>
      <AnnotatedResult imageUrl={res.annotated_path} />
    </div>
  ))}
</div>       
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default TrayCounting;
