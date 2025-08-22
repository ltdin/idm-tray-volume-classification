function ResultTable({ data }) {
  if (!Array.isArray(data)) return <p>No rack data available.</p>;

  const sorted = [...data].sort((a, b) => {
    const aWarn = String(a.status || '').toUpperCase() === 'WARN' ? 0 : 1;
    const bWarn = String(b.status || '').toUpperCase() === 'WARN' ? 0 : 1;
    if (aWarn !== bWarn) return aWarn - bWarn;
    return (a.order ?? 0) - (b.order ?? 0);
  });

  const statusStyle = (status) => {
    const s = String(status || '').toUpperCase();
    return {
      color: s === 'WARN' ? '#c62828' : '#2e7d32',
      fontWeight: 700,
    };
  };

  return (
    <div style={{ marginTop: '2rem' }}>
       <h3 style={{ color: '#0068b5' }}>Result Table</h3>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Name</th>
            <th>Status</th>
            <th>Wheels</th>
            <th>Out</th>
            <th>In</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((rack, index) => (
            <tr key={index}>
              <td>{rack.filename}</td>
              <td style={statusStyle(rack.status)}>{String(rack.status || '').toUpperCase()}</td>
              <td>{rack.num_wheels}</td>
              <td>{rack.out}</td>
              <td>{rack.in}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ResultTable;
