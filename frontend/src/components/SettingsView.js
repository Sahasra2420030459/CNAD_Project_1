import React, { useState, useEffect } from 'react';
import { healthApi, getApiBaseUrl, setCustomApiBaseUrl } from '../services/api';

const SettingsView = () => {
  const [healthData, setHealthData] = useState(null);
  const [loadingHealth, setLoadingHealth] = useState(false);
  const [pingLatency, setPingLatency] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [customUrlInput, setCustomUrlInput] = useState(getApiBaseUrl());

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

  const handleSaveUrl = () => {
    setCustomApiBaseUrl(customUrlInput);
    checkServerHealth();
  };

  useEffect(() => {
    checkServerHealth();
  }, []);

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', paddingBottom: '3rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#fff' }}>Environment & Architecture</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
            System configuration, active service bindings, and microservice status.
          </p>
        </div>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={checkServerHealth}
          disabled={loadingHealth}
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
        >
          <span>{loadingHealth ? '🔄' : '⚡'}</span>
          {loadingHealth ? 'Probing...' : 'Ping Backend'}
        </button>
      </div>

      {feedback && (
        <div className={`alert-box alert-${feedback.type}`} style={{ marginBottom: '1.5rem' }}>
          <span>{feedback.type === 'success' ? '✅' : '⚠️'} {feedback.text}</span>
          <button
            type="button"
            className="btn-remove-staged"
            onClick={() => setFeedback(null)}
            style={{ marginLeft: 'auto' }}
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
            Active Backend Target
          </div>
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <input
              type="text"
              value={customUrlInput}
              onChange={(e) => setCustomUrlInput(e.target.value)}
              placeholder="https://your-backend.onrender.com"
              className="select-control"
              style={{ flex: 1, padding: '0.4rem 0.6rem', fontSize: '0.8rem' }}
            />
            <button
              type="button"
              className="btn btn-primary"
              style={{ padding: '0.4rem 0.75rem', fontSize: '0.8rem' }}
              onClick={handleSaveUrl}
            >
              Update
            </button>
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
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
            {healthData?.queueAdapter || 'IN_MEMORY_EVENT_DISPATCHER'}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
            Local development uses JVM in-memory blocking queue; production uses Azure Storage Queue.
          </div>
        </div>

        {/* Background Worker */}
        <div style={{ background: 'var(--bg-input)', padding: '1.25rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fff', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span>⚙️</span> Video Compression Engine
          </h3>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
            Transcoder Engine State
          </div>
          <div style={{
            background: 'rgba(0,0,0,0.3)',
            padding: '0.6rem 0.85rem',
            borderRadius: 'var(--radius-sm)',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.8rem',
            color: 'var(--accent-primary)',
          }}>
            {healthData?.ffmpegAvailable ? 'FFmpeg Transcoder Active' : 'Simulation Mode (FFmpeg missing on host)'}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
            Worker runs within the multi-stage Docker environment with hardware/software H.264 codecs.
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsView;
