function ResultTable({ data }) {
  if (!Array.isArray(data)) return <p>No rack data available.</p>;

  return (
    <div style={{ marginTop: '2rem' }}>
       <h3 style={{ color: '#0068b5' }}>Result Table</h3>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Rack ID</th>
            <th>Volume (%)</th>
            <th>Quantity (Max: 1161)</th>
          </tr>
        </thead>
        <tbody>
          {data.map((rack, index) => (
            <tr key={index}>
              <td>{rack.rack_id}</td>
              <td>{rack.volume.toFixed(2)}</td>
              <td>{rack.quantity}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ResultTable;