import React, { useState } from 'react';
import NavBar from './components/NavBar';
import HomePage from './pages/HomePage';
import TrayCountingPage from './pages/TrayCountingPage';
import handleOptionSelect from './handlers/handleOptionSelect';
import KanbanPage from './pages/KanbanPage';
import IDMFineTunePage from './pages/IDMFineTunePage';

function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [images, setImages] = useState([]);
  const [previews, setPreviews] = useState([]);
  const [results, setResults] = useState([]);
  const [rackIdImage, setRackIdImage] = useState(null);
  const [rackIdText, setRackIdText] = useState('');

  return (
    <div
      style={{
        fontFamily: 'Arial, sans-serif',
        backgroundColor: '#f6f8fa',
        minHeight: '100vh',
      }}
    >
      <NavBar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        onOptionSelect={(option) => handleOptionSelect(option, setActiveTab)}
      />

      {activeTab === 'tray' && (
        <TrayCountingPage
          images={images}
          setImages={setImages}
          previews={previews}
          setPreviews={setPreviews}
          results={results}
          setResults={setResults}
          rackIdImage={rackIdImage}
          setRackIdImage={setRackIdImage}
          rackIdText={rackIdText}
          setRackIdText={setRackIdText}
        />
      )}

      {activeTab === 'kanban' && <KanbanPage />}

      {activeTab === 'home' && <HomePage />}

      {activeTab === 'fine-tune' && <IDMFineTunePage />}
    </div>
  );
}

export default App;
