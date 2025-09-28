import React, { useState, useEffect } from "react";

export default function SentimentList() {
  const [locations, setLocations] = useState([]);
  const [sortBy, setSortBy] = useState("overall");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function fetchData(sortKey) {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`http://127.0.0.1:5000/sort?by=${sortKey}`);
      if (!res.ok) throw new Error("Failed to fetch data from API");
      const data = await res.json();
      setLocations(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchData(sortBy);
  }, [sortBy]);

  return (
    <div>
      <h2 style={{ textAlign: "center", marginBottom: "20px" }}>Locations Sorted by Sentiments</h2>

      <label>
        Sort by:{" "}
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="overall">Overall</option>
          <option value="maintenance">Maintenance</option>
          <option value="distance">Distance</option>
          <option value="environment">Environment</option>
        </select>
      </label>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      <ul style={{ listStyleType: "none", padding: 0 }}>
        {locations.map((loc) => (
          <li
            key={loc.location}
            style={{
              display: "flex",
              alignItems: "center",
              marginBottom: "20px",
              border: "1px solid #000000ff",
              padding: "10px",
              borderRadius: "8px",
            }}
          >
            <img
              src={loc.image_url}
              alt={loc.location}
              style={{ width: "20%", height: "auto", objectFit: "cover", marginRight: "20px", borderRadius: "6px" }}
            />
            <div>
              <strong>{loc.location}</strong>
              <p>
                Overall: {loc.overall_sentiment}, Maintenance: {loc.maintenance_sentiment}, Distance: {loc.distance_sentiment}, Environment: {loc.environment_sentiment}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
