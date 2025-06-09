function NavBar({ activeTab, onTabChange }) {
  const navStyle = {
    backgroundColor: '#ffffff',
    borderBottom: '2px solid #0068b5',
    padding: '1rem 2rem',
    color: 'white',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  };

  const tabStyle = (tab) => ({
    marginLeft: '1rem',
    padding: '0.5rem 1rem',
    borderRadius: '6px',
    backgroundColor: activeTab === tab ? '#0068b5' : 'transparent',
    cursor: 'pointer',
    color: activeTab === tab ? 'white' : '#0068b5',
    border: '1px solid white'
  });

  return (
    <div style={navStyle}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/64/Intel-logo-2022.png" alt="Intel" height="28" />
      </div>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <div onClick={() => onTabChange('tray')} style={tabStyle('tray')}>IDM Tray Counting</div>
        <div onClick={() => onTabChange('kanban')} style={tabStyle('kanban')}>Kanban Checking</div>
      </div>
    </div>
  );
}

export default NavBar;
