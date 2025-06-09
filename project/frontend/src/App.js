import React, { useState } from 'react';
import NavBar from './IDM Tray Counting/components/NavBar';
import UploadForm from './IDM Tray Counting/components/UploadForm';
import ImagePreview from './IDM Tray Counting/components/ImagePreview';
import AnnotatedResult from './IDM Tray Counting/components/AnnotatedResult';
import ResultTable from './IDM Tray Counting/components/ResultTable';
import handleImageChange from './IDM Tray Counting/handlers/handleImageChange';
import handleSubmit from './IDM Tray Counting/handlers/handleSubmit';

function App() {
  const [activeTab, setActiveTab] = useState('tray');
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', backgroundColor: '#f6f8fa', minHeight: '100vh' }}>
      <NavBar activeTab={activeTab} onTabChange={setActiveTab} />

      {activeTab === 'tray' ? (
        <div style={{ padding: '2rem', display: 'flex', gap: '2rem' }}>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            <div style={{ background: '#fff', padding: '2rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
              <UploadForm
                onImageChange={(file) => handleImageChange(file, setImage, setPreview, setResult)}
                onSubmit={() => handleSubmit(image, setResult)}
              />
              {preview && <ImagePreview src={preview} />}
            </div>

            {result && (
              <div style={{ background: '#fff', padding: '1rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
                <AnnotatedResult imageUrl={result.annotated_path} />
              </div>
            )}
          </div>

          {result && (
            <div style={{ flex: 1 }}>
              <div style={{ background: '#fff', padding: '2rem', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
                <ResultTable data={result.racks} />
              </div>
            </div>
          )}
        </div>
      ) : (
        <div style={{ padding: '2rem', textAlign: 'center' }}>
          <h2>🔧 Kanban Checking – Coming Soon</h2>
        </div>
      )}
    </div>
  );
}

export default App;
