import React, { useState, useMemo } from 'react';
import UploadForm from '../components/Kanban Zone/UploadForm';
import AnnotatedResult from '../components/IDM Tray Counting/AnnotatedResult'; 
import ResultTable from '../components/Kanban Zone/ResultTable';
import ImagePreviewPanel from '../components/IDM Tray Counting/ImagePreviewPanel';
import handleImageChange from '../handlers/IDM Tray Counting/handleImageChange';
import handleSubmit from '../handlers/Kanban Zone/handleSubmit';

function KanbanPage() {
  const [images, setImages] = useState([]);
  const [previews, setPreviews] = useState([]);
  const [results, setResults] = useState([]);

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
        <div style={{ display: 'flex', gap: '2rem', alignItems: 'flex-start' }}>
          <div style={{ flex: 1 }}>
            <UploadForm
              onImageChange={(files) =>
                handleImageChange(files, setImages, setPreviews, setResults)
              }
              onSubmit={() => handleSubmit(images, setResults)}
            />
          </div>

          <div style={{ flex: 2, paddingLeft: '2rem', borderLeft: '2px solid #e0e0e0' }}>
            <ImagePreviewPanel previewUrls={previews} yoloImages={images} />
          </div>
          {results.length > 0 && (
            <>
            {/* Table */}
          <div>
            <ResultTable data={results} />
          </div>
            </>
          )}
        </div>
      </div>
 
      {results.length > 0 && (
        <>
          {/* Annotated images grid */}
          <div
            style={{
              background: '#fff',
              padding: '2rem',
              borderRadius: '12px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              marginBottom: '2rem',
            }}
          >
            <h3 style={{ marginTop: 0, color: '#0068b5' }}>Annotated Results</h3>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
                gap: '1rem',
              }}
            >
              {results.map((res, idx) => (
                <div key={idx}>
                  <AnnotatedResult imageUrl={res.annotated_path} />
                  <div style={{ marginTop: '0.5rem', fontSize: '0.85rem' }}>
                    <div><b>{res.filename || `Image #${res.order}`}</b></div>
                    <div>
                      Status:{' '}
                      <span
                        style={{
                          padding: '2px 8px',
                          borderRadius: '999px',
                          color:
                            (res.status || '').toLowerCase() === 'safe' ? '#2e7d32' : '#c62828',
                          fontWeight: 600,
                        }}
                      >
                        {(res.status || '').toUpperCase()}
                      </span>
                      {' '}• Wheels: {res.num_wheels} • IN: {res.in ?? 0} • OUT: {res.out ?? 0}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default KanbanPage;
