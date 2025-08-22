import React, { useEffect, useState } from 'react';
import axios from 'axios';
import DeleteOutlineRoundedIcon from '@mui/icons-material/DeleteOutlineRounded';
import AdsClickRoundedIcon from '@mui/icons-material/AdsClickRounded';
import ExpandMoreRoundedIcon from '@mui/icons-material/ExpandMoreRounded';

function ModelVersionsPanel() {
  const [versions, setVersions] = useState([]);
  const [isListOpen, setIsListOpen] = useState(false);
  const [expandedVersion, setExpandedVersion] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadVersions = async () => {
    try {
      const res = await axios.get('http://localhost:5001/api/model/versions');
      setVersions(res.data);
    } catch (error) {
      console.error(error);
      setVersions([]);
    }
  };

  useEffect(() => {
    loadVersions();
  }, []);

  const handleUseVersion = async (version_name) => {
    setLoading(true);
    await axios.post('http://localhost:5001/api/model/use-version', { version_name });
    await loadVersions();
    setExpandedVersion(null);
    setLoading(false);
  };

  const handleDeleteVersion = async (version_name) => {
    if (!window.confirm('Are you sure you want to delete this version?')) return;
    setLoading(true);
    await axios.post('http://localhost:5001/api/model/delete-version', { version_name });
    await loadVersions();
    setExpandedVersion(null);
    setLoading(false);
  };

  const fileUrl = (path) => {
    if (!path) return "";
    return `http://localhost:5001${path.replace("..", "")}`;
  };

  const round = (val) => {
    if (val == null) return "-";
    return Number(val).toFixed(3);
  };

  return (
    <div style={{ marginTop: '2rem' }}>
      <button
        style={{
          background: '#ffffff',
          color: '#0068b5',
          border: '1px solid #0068b5',
          borderRadius: '30px',
          padding: '0.5rem 1rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          fontWeight: 'bold',
          cursor: 'pointer',
          transition: 'all 0.3s ease'
        }}
        onClick={() => setIsListOpen(!isListOpen)}
        onMouseOver={e => e.currentTarget.style.background = '#e6f2fa'}
        onMouseOut={e => e.currentTarget.style.background = '#f1f1f1'}
      >
        <ExpandMoreRoundedIcon
          style={{
            transform: isListOpen ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: 'transform 0.3s ease'
          }}
        />
        {isListOpen ? 'Hide Model Versions' : 'View All Model Versions'}
      </button>

      {isListOpen && (
        <div style={{
          marginTop: '1rem',
          background: '#fff',
          borderRadius: '8px',
          padding: '1rem',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          {versions.length === 0 && <p>No versions found.</p>}

          {versions.map((ver) => (
            <div key={ver.version_name} style={{
              borderBottom: '1px solid #eee',
              padding: '1.5rem 0'
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <div style={{ fontSize: '1.1rem' }}>
                  {ver.version_name}
                  {ver.is_current && (
                    <span style={{
                      fontWeight: 'bold',
                      background: '#28a745',
                      color: '#fff',
                      padding: '2px 8px',
                      marginLeft: '10px',
                      borderRadius: '8px',
                      fontSize: '0.8rem'
                    }}>USING</span>
                  )}
                </div>
                <button
                  style={{
                    background: '#0068b5',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '4px',
                    padding: '0.5rem 1rem',
                    cursor: 'pointer'
                  }}
                  onClick={() => setExpandedVersion(
                    expandedVersion === ver.version_name
                      ? null
                      : ver.version_name
                  )}
                >
                  {expandedVersion === ver.version_name ? '▲' : '▼'}
                </button>
              </div>

              {expandedVersion === ver.version_name && (
                <div style={{
                  marginTop: '1rem',
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '2rem'
                }}>
                  <div>
                    <h4 style={{ marginBottom: '0.5rem', color: '#0068b5' }}>YOLO Metrics</h4>
                    <table style={tableStyle}>
                      <tbody>
                        <tr><td style={cellStyle}>mAP50</td><td style={cellStyle}>{round(ver.metrics?.mAP50)}</td></tr>
                        <tr><td style={cellStyle}>mAP50-95</td><td style={cellStyle}>{round(ver.metrics?.['mAP50-95'])}</td></tr>
                        <tr><td style={cellStyle}>Precision</td><td style={cellStyle}>{round(ver.metrics?.precision)}</td></tr>
                        <tr><td style={cellStyle}>Recall</td><td style={cellStyle}>{round(ver.metrics?.recall)}</td></tr>
                      </tbody>
                    </table>

                    <h4 style={{ margin: '1.5rem 0 0.5rem', color: '#0068b5' }}>CNN Metrics</h4>
                    {ver.cnn_metrics ? (
                      <table style={tableStyle}>
                        <tbody>
                          <tr><td style={cellStyle}>Loss</td><td style={cellStyle}>{round(ver.cnn_metrics?.loss?.[0])}</td></tr>
                          <tr><td style={cellStyle}>Val Loss</td><td style={cellStyle}>{round(ver.cnn_metrics?.val_loss?.[0])}</td></tr>
                          <tr><td style={cellStyle}>MAE</td><td style={cellStyle}>{round(ver.cnn_metrics?.mae?.[0])}</td></tr>
                          <tr><td style={cellStyle}>Val MAE</td><td style={cellStyle}>{round(ver.cnn_metrics?.val_mae?.[0])}</td></tr>
                        </tbody>
                      </table>
                    ) : (
                      <p style={{ color: '#888' }}>CNN metrics not available.</p>
                    )}
                  </div>

                  <div>
                    <h4 style={{ marginBottom: '0.5rem', color: '#0068b5' }}>YOLO Plots</h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      {ver.files?.F1_curve && (
                        <img
                          src={fileUrl(ver.files.F1_curve)}
                          alt="F1 Curve"
                          style={plotStyle}
                        />
                      )}
                      {ver.files?.R_curve && (
                        <img
                          src={fileUrl(ver.files.R_curve)}
                          alt="R Curve"
                          style={plotStyle}
                        />
                      )}
                    </div>
                  </div>
                </div>
              )}

              {expandedVersion === ver.version_name && (
                <div style={{
                  marginTop: '1rem',
                  display: 'flex',
                  gap: '1rem'
                }}>
                  {!ver.is_current && (
                    <>
                      <button style={btn} onClick={() => handleUseVersion(ver.version_name)}>
                        <AdsClickRoundedIcon style={{ fontSize: '1rem', marginRight: '0.5rem' }} />
                        Use this version
                      </button>
                      <button
                        style={{ ...btn, background: '#dc3545' }}
                        onClick={() => handleDeleteVersion(ver.version_name)}
                      >
                        <DeleteOutlineRoundedIcon style={{ fontSize: '1rem', marginRight: '0.5rem' }} />
                        Delete
                      </button>
                    </>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const tableStyle = {
  borderCollapse: 'collapse',
  width: '100%',
};

const cellStyle = {
  border: '1px solid #ddd',
  padding: '8px',
  fontSize: '0.9rem'
};

const plotStyle = {
  width: '300px',
  borderRadius: '8px',
  border: '1px solid #ddd'
};

const btn = {
  background: '#0068b5',
  color: '#fff',
  border: 'none',
  borderRadius: '4px',
  padding: '0.5rem 1rem',
  cursor: 'pointer'
};

export default ModelVersionsPanel;
