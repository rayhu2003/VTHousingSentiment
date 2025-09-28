import React, { useState, useEffect } from "react";
import './Sentiment.css';

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

  // A utility function to convert sentiment to width percentage for horizontal bars
  const sentimentToWidth = (sentiment) => {
    return `${(sentiment / 10) * 100}%`;  // Assuming sentiment is a number between 1 and 10
  };

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
            className="sentiment-card"
            style={{
              display: "flex",
              alignItems: "center",
              marginBottom: "20px",
              border: "1px solid #000000ff",
              padding: "10px",
              borderRadius: "8px",
              opacity: 1,
            }}
          >
            <a
              href={loc.website_url}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: "flex",
                alignItems: "center",
                textDecoration: "none",
                color: "inherit",
                width: "100%",
              }}
            >
              <img
                src={loc.image_url}
                alt={loc.location}
                style={{
                  width: "20%",
                  height: "auto",
                  objectFit: "cover",
                  marginRight: "20px",
                  borderRadius: "6px",
                  cursor: "pointer",
                }}
              />
              <div style={{ flex: 2, textAlign: "left" }}>
                {/* Name of the complex (bigger font size) */}
                <strong style={{ cursor: "pointer", fontSize: "24px" }}>
                  {loc.location}
                </strong>
                
                {/* Sentiment numbers (bigger font size) */}
                <p style={{ fontSize: "20px", lineHeight: "1.6" }}>
                  Overall: <strong>{loc.overall_sentiment}</strong>, 
                  Maintenance: <strong>{loc.maintenance_sentiment}</strong>, 
                  Distance: <strong>{loc.distance_sentiment}</strong>, 
                  Environment: <strong>{loc.environment_sentiment}</strong>
                </p>

                {/* Render categories and bars horizontally */}
                <div style={{ display: "flex", flexDirection: "column", marginLeft: "20px" }}>
                  {/* Overall Sentiment Bar */}
                  <div style={{ display: "flex", marginBottom: "10px" }}>
                    <span style={{ width: "120px", textAlign: "right", paddingRight: "10px" }}>Overall</span>
                    <div
                      style={{
                        width: sentimentToWidth(loc.overall_sentiment),
                        height: "20px",
                        backgroundColor: "#2196F3",
                        borderRadius: "4px",
                      }}
                    ></div>
                  </div>

                  {/* Maintenance Sentiment Bar */}
                  <div style={{ display: "flex", marginBottom: "10px" }}>
                    <span style={{ width: "120px", textAlign: "right", paddingRight: "10px" }}>Maintenance</span>
                    <div
                      style={{
                        width: sentimentToWidth(loc.maintenance_sentiment),
                        height: "20px",
                        backgroundColor: "#2196F3",
                        borderRadius: "4px",
                      }}
                    ></div>
                  </div>

                  {/* Distance Sentiment Bar */}
                  <div style={{ display: "flex", marginBottom: "10px" }}>
                    <span style={{ width: "120px", textAlign: "right", paddingRight: "10px" }}>Distance</span>
                    <div
                      style={{
                        width: sentimentToWidth(loc.distance_sentiment),
                        height: "20px",
                        backgroundColor: "#2196F3",
                        borderRadius: "4px",
                      }}
                    ></div>
                  </div>

                  {/* Environment Sentiment Bar */}
                  <div style={{ display: "flex", marginBottom: "10px" }}>
                    <span style={{ width: "120px", textAlign: "right", paddingRight: "10px" }}>Environment</span>
                    <div
                      style={{
                        width: sentimentToWidth(loc.environment_sentiment),
                        height: "20px",
                        backgroundColor: "#2196F3",
                        borderRadius: "4px",
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
