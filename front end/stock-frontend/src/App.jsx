/* === src/App.jsx === */
/* This version is updated to connect to a REAL Python backend. */

import React, { useState } from 'react';
import { Search, BarChart2 } from 'lucide-react';
import './App.css'; // Import the stylesheet

export default function App() {
  const [ticker, setTicker] = useState('');
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // The mockFetch function has been REMOVED.
  // We will now call the real backend.

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!ticker) {
      setError("Please enter a stock ticker.");
      return;
    }
    setError('');
    setData(null);
    setLoading(true);

    try {
      // --- IMPORTANT CHANGE ---
      // The line below now calls your actual Python backend server.
      // Make sure your Python Flask/FastAPI server is running.
      const response = await fetch(`http://127.0.0.1:5000/predict?ticker=${ticker}`);

      if (!response.ok) {
        // This will handle errors sent from your Python backend
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to fetch data from the server.");
      }

      // The backend should return JSON in this format:
      // {
      //   "companyName": "Apple Inc.",
      //   "ticker": "AAPL",
      //   "price": 178.69,
      //   "prediction": {
      //     "value": 182.50,
      //     "trend": "Bullish 🐂"
      //   }
      // }
      const result = await response.json();
      setData(result);

    } catch (err) {
      // This will catch network errors (e.g., if the server is not running)
      // or errors thrown from the response check above.
      setError(err.message || "An unknown fetch error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="content-wrapper">
        <h1 className="main-title">
          Stock Market Predictor
        </h1>
        <p className="subtitle">
          Enter a US stock ticker for an AI-powered prediction.
        </p>

        <form onSubmit={handleSearch} className="search-form">
          <Search className="search-icon" />
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="e.g. AAPL, TSLA, GOOG"
            className="search-input"
          />
          <button
            type="submit"
            disabled={loading}
            className="search-button"
          >
            {loading ? '...' : 'Predict'}
          </button>
        </form>

        <div className="results-area">
          {loading && (
            <div className="loader-container">
              <div className="spinner"></div>
              <p>Fetching Market Data...</p>
            </div>
          )}
          {error && (
            <div className="error-message">
              <p>❌ {error}</p>
            </div>
          )}
          {!loading && !error && !data && (
            <div className="placeholder">
              <BarChart2 size={40} />
              <p>Prediction results will appear here</p>
            </div>
          )}
          {data && (
            <div className="output-card">
              <h2 className="output-title">{data.companyName} ({data.ticker})</h2>
              <div className="output-row">
                <p>Current Price:</p>
                <p className="price-value">${data.price}</p>
              </div>
              <div className="output-row prediction-row">
                <p>AI Prediction:</p>
                <p className={`price-value ${data.prediction?.trend.includes('Bullish') ? 'trend-bullish' : 'trend-bearish'}`}>
                  ${data.prediction?.value} — {data.prediction?.trend}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
