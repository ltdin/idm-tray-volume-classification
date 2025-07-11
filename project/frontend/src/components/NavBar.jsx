import React, { useState, useEffect, useRef } from 'react';

function NavBar({ onOptionSelect }) {
  const [openTab, setOpenTab] = useState(null);
  const navRef = useRef();

  const tabs = [
    { key: 'masterprogram', label: 'MASTER PROGRAM' },
    { key: 'support', label: 'SUPPORT' },
    { key: 'solutions', label: 'SOLUTIONS' },
    
  ];

  const megaMenuContent = {
    masterprogram: [
      { title: 'IDM Inventory Management', items: ['Fine Tune Model','Validation'] },
      { title: '5S Auto Audit', items: ['Training/Fine Tune Model', 'Validation'] },
      { title: 'Settings Robot Schedule ', items: ['Dynamic Boston Spot'] },
    ],
    support: [
      { title: 'Drivers & Downloads', items: ['Auto-update your Drivers', 'Download Center'] },
      { title: 'Support For', items: ['Products', 'Developers', 'Suppliers'] }
    ],
    solutions: [
      { title: 'Industries', items: ['Automotive', 'Education','Energy','Financial Services', 'Government'] }
    ]
  };

  const navStyle = {
    display: 'flex',
    alignItems: 'center',
    padding: '0.8rem 2rem',
    backgroundColor: '#fff',
    borderBottom: '2px solid #0068b5',
    position: 'relative'
  };

  const getTabStyle = (key) => ({
    padding: '0.5rem 1rem',
    color: openTab === key ? '#000' : '#0068b5',
    fontSize: '0.9rem',
    cursor: 'pointer',
    position: 'relative',
    borderBottom: openTab === key ? '2px solid #0068b5' : '2px solid transparent',
    fontWeight: openTab === key ? 'bold' : 'normal'
  });

  const megaMenuStyle = {
    position: 'absolute',
    top: '100%',
    left: '0',
    width: '100%',
    backgroundColor: '#fff',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
    display: openTab && megaMenuContent[openTab] ? 'flex' : 'none',
    padding: '1rem 4rem',
    zIndex: 10,
    justifyContent: 'flex-start',
    gap: '3rem',
    flexWrap: 'wrap'
  };

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (navRef.current && !navRef.current.contains(e.target)) {
        setOpenTab(null);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleTabClick = (key) => {
    setOpenTab(prev => (prev === key ? null : key));
  };

  return (
    <div style={navStyle} ref={navRef}>
      <img
        src="https://upload.wikimedia.org/wikipedia/commons/6/64/Intel-logo-2022.png"
        alt="Intel"
        height="28"
        style={{ cursor: 'pointer', marginRight: '2rem' }}
        onClick={() => onOptionSelect({ section: 'home', item: 'home' })}
      />
      {tabs.map(tab => (
        <div
          key={tab.key}
          style={getTabStyle(tab.key)}
          onClick={() => handleTabClick(tab.key)}
        >
          {tab.label}
        </div>
      ))}

      {openTab && megaMenuContent[openTab] && (
        <div style={megaMenuStyle}>
          {megaMenuContent[openTab].map((col, idx) => (
            <div key={idx} style={{ minWidth: '150px' }}>
              <p style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>{col.title}</p>
              <ul style={{ fontSize: '0.8rem', color: '#0068b5', listStyle: 'none', padding: 0, margin: 0 }}>
                {col.items.map((item, i) => (
                  <li
                    key={i}
                    style={{ padding: '0.2rem 0', cursor: 'pointer', fontSize: '0.9rem' }}
                    onClick={() => onOptionSelect({
                      section: openTab,
                      title: col.title,
                      item
                    })}
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default NavBar;
