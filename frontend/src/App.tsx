// src/App.tsx
import { useState, useEffect } from 'react';

// Simple inline styles as fallback
const styles = {
  container: {
    padding: '2rem',
    maxWidth: '800px',
    margin: '0 auto',
    fontFamily: 'Arial, sans-serif'
  },
  heading: {
    fontSize: '2rem',
    fontWeight: 'bold',
    textAlign: 'center' as const,
    marginBottom: '1rem'
  },
  statusBox: {
    padding: '1rem',
    border: '1px solid #ddd',
    borderRadius: '8px',
    margin: '1rem 0',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  },
  button: {
    padding: '0.5rem 1rem',
    margin: '0.5rem',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  error: {
    color: 'red',
    backgroundColor: '#ffe6e6',
    padding: '1rem',
    borderRadius: '4px',
    margin: '1rem 0'
  }
};

function App() {
  const [message, setMessage] = useState<string>('');
  const [health, setHealth] = useState<string>('Checking...');
  const [error, setError] = useState<string | null>(null);

  const fetchMessage = async () => {
    try {
      setError(null);
      const response = await fetch('http://localhost:8000/');
      if (!response.ok) {
        throw new Error(`Backend responded with status: ${response.status}`);
      }
      const data = await response.json();
      setMessage(data.message);
    } catch (error) {
      console.error("Failed to fetch from backend:", error);
      setError("Could not connect to the backend. Please ensure it is running on port 8000.");
      setMessage("");
    }
  };

  const checkHealth = async () => {
    try {
      setError(null);
      const response = await fetch('http://localhost:8000/health');
      if (!response.ok) {
        throw new Error(`Health check failed with status: ${response.status}`);
      }
      const data = await response.json();
      setHealth(data.status);
    } catch (error) {
      console.error("Failed to fetch health:", error);
      setError("Health check failed. Is the backend server running?");
      setHealth("unhealthy");
    }
  };

  useEffect(() => {
    fetchMessage();
    checkHealth();
  }, []);

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>🧠 Intelligent Development Assistant</h1>
      
      <p style={{textAlign: 'center', fontSize: '1.1rem'}}>
        Dashboard for AI-powered code analysis and documentation.
      </p>

      {error && (
        <div style={styles.error}>
          ⚠️ {error}
        </div>
      )}

      <div style={styles.statusBox}>
        <p><strong>Backend Status:</strong> 
          <span style={{ 
            color: health === 'healthy' ? 'green' : 'red',
            fontWeight: 'bold',
            marginLeft: '0.5rem'
          }}>
            {health}
          </span>
        </p>
        <p><strong>API Message:</strong> {message || 'No message received'}</p>
      </div>

      <div style={{textAlign: 'center'}}>
        <button 
          style={{...styles.button, backgroundColor: '#3182ce', color: 'white'}}
          onClick={fetchMessage}
        >
          Refresh Message
        </button>
        <button 
          style={{...styles.button, backgroundColor: '#38a169', color: 'white'}}
          onClick={checkHealth}
        >
          Check Health
        </button>
      </div>

      <p style={{textAlign: 'center', color: '#666', fontSize: '0.9rem', marginTop: '2rem'}}>
        Next steps: GitHub integration, code upload, and AI analysis.
      </p>
    </div>
  );
}

export default App;