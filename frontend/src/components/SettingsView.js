import React, { useState, useEffect } from 'react';
import { healthApi } from '../services/api';

const SettingsView = () => {
  const [healthData, setHealthData] = useState(null);
  const [loadingHealth, setLoadingHealth] = useState(false);
  const [pingLatency, setPingLatency] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const checkServerHealth = async () => {
    setLoadingHealth(true);
    setFeedback(null);
    const start = performance.now();
    try {
      const data = await healthApi.checkHealth();
      const latency = Math.round(performance.now() - start);
      setHealthData(data);
      setPingLatency(latency);
      setFeedback({ type: 'success', text: `Backend reachable (${latency}ms)!` });
    } catch (err) {
      setFeedback({ type: 'danger', text: 'Backend is currently offline or unreachable.' });
    } finally {
      setLoadingHealth(false);
    }
  };

  useEffect(() => {
    checkServerHealth();
  }, []);

  return (
    <div className="card-panel">
      <div className="panel-header">
        <div>
          <h2 className="panel-title">System & Cloud Settings</h2>
          <p className="panel-subtitle">
            Inspect active cloud adapters, FFmpeg transcoding engine, and REST API connectivity.
          </p>
        </div>
        <button
          type="button"
          className="btn btn-outline btn-xs"
          onClick={checkServerHealth}
          disabled={loadingHealth}
        >
          {loadingHealth ? 'Pinging...' : '⚡ Ping Health Check'}
        </button>
      </div>

      {feedback && (
        <div className={`alert-box alert-${feedback.type}`} role="status">
          <span>{feedback.text}</span>
          <button
            type="button"
            className="logout-icon-btn"
            onClick={() => setFeedback(null)}
            aria-label="Dismiss feedback"
          >
            &times;
          </button>
        </div>
      )}

      {/* Grid of configuration sections */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
        {/* Runtime Connectivity */}
        <div style={{ background: 'var(--bg-input)', padding: '1.25rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>🌐</span> REST API Endpoint
          </h3>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
            Configured via <code>REACT_APP_API_BASE_URL</code>
          </div>
          <div style={{
            background: 'rgba(0,0,0,0.3)',
            padding: '0.6rem 0.85rem',
            borderRadius: 'var(--radius-sm)',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.8rem',
            color: 'var(--accent-cyan)',
            wordBreak: 'break-all'
          }}>
            {process.env.REACT_APP_API_BASE_URL || 'http://localhost:8080/api'}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
            Status: {healthData ? 'ONLINE' : 'PENDING'} {pingLatency ? `(${pingLatency} ms)` : ''}
          </div>
        </div>

        {/* Storage Adapter */}
        <div style={{ background: 'var(--bg-input)', padding: '1.25rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>🗄️</span> Video Storage Adapter
          </h3>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
            Active Provider (Controlled by <code>STORAGE_TYPE</code>)
          </div>
          <div style={{
            background: 'rgba(0,0,0,0.3)',
            padding: '0.6rem 0.85rem',
            borderRadius: 'var(--radius-sm)',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.8rem',
            color: 'var(--accent-emerald)',
          }}>
            {healthData?.storageAdapter || 'LOCAL_DISK'}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
            Local development uses disk directory <code>./uploads</code>; production points to Azure Blob Container <code>video-processing</code>.
          </div>
        </div>

        {/* Queue Adapter */}
        <div style={{ background: 'var(--bg-input)', padding: '1.25rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>📬</span> Asynchronous Message Queue
          </h3>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
            Active Queue (Controlled by <code>QUEUE_TYPE</code>)
          </div>
          <div style={{
            background: 'rgba(0,0,0,0.3)',
            padding: '0.6rem 0.85rem',
            borderRadius: 'var(--radius-sm)',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.8rem',
            color: 'var(--accent-amber)',
          }}>
            {healthData?.queueAdapter || 'LOCAL_IN_MEMORY'} (Depth: {healthData?.queueDepth ?? 0})
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
            Decouples HTTP requests from CPU transcoding. Scales with Azure Container Apps KEDA rules.
          </div>
        </div>

        {/* Security & Authentication Policy */}
        <div style={{ background: 'var(--bg-input)', padding: '1.25rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>🔒</span> Security & Token Policy
          </h3>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
            In-Memory Token Storage (Strict Isolation)
          </div>
          <p style={{ fontSize: '0.775rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
            To prevent cross-site scripting (XSS) credential theft, authentication tokens are stored exclusively in memory and session scope. <code>localStorage</code> persistence is disabled.
          </p>
        </div>
      </div>
    </div>
  );
};

export default SettingsView;
