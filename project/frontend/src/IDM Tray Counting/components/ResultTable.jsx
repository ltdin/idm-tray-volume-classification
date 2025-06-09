function ResultTable({ data }) {
  if (!Array.isArray(data)) return <p>No rack data available.</p>;

  return (
    <div style={{ marginTop: '2rem' }}>
      <h4>Prediction Table:</h4>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Rack ID</th>
            <th>Volume (%)</th>
          </tr>
        </thead>
        <tbody>
          {data.map((rack, index) => (
            <tr key={index}>
              <td>{rack.rack_id}</td>
              <td>{rack.volume.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ResultTable;