import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { getApiBaseUrl, setCustomApiBaseUrl } from '../services/api';

const AuthModal = ({ isOpen, onClose, initialMode = 'login' }) => {
  const [mode, setMode] = useState(initialMode);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState(null);
  const [isNetworkError, setIsNetworkError] = useState(false);
  const [backendUrlInput, setBackendUrlInput] = useState(getApiBaseUrl());
  const [loading, setLoading] = useState(false);

  const { login, register } = useAuth();

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsNetworkError(false);
    setLoading(true);

    try {
      if (mode === 'login') {
        await login(email, password);
      } else {
        await register(email, password, fullName);
      }
      onClose();
    } catch (err) {
      const serverMsg = err.response?.data?.message || err.response?.data?.details?.[0];
      if (serverMsg) {
        setError(serverMsg);
      } else if (!err.response || err.message === 'Network Error' || err.code === 'ERR_NETWORK') {
        setIsNetworkError(true);
        setError(`Cannot reach backend API at: ${getApiBaseUrl()}. Please verify your backend URL below.`);
      } else {
        setError('Authentication failed. Please verify credentials.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSaveBackendUrl = () => {
    if (backendUrlInput && backendUrlInput.trim()) {
      setCustomApiBaseUrl(backendUrlInput);
      setError(null);
      setIsNetworkError(false);
    }
  };

  return (
    <div
      className="modal-overlay"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="auth-modal-title"
    >
      <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
          <h2 id="auth-modal-title" style={{ fontSize: '1.3rem', fontWeight: 700, color: '#fff' }}>
            {mode === 'login' ? 'Sign In to VideoCloud' : 'Create Student Account'}
          </h2>
          <button
            type="button"
            className="btn-remove-staged"
            onClick={onClose}
            aria-label="Close dialog"
            style={{ fontSize: '1.5rem' }}
          >
            &times;
          </button>
        </div>

        {/* Tab Switcher */}
        <div style={{ display: 'flex', borderBottom: '1px solid var(--border-subtle)', marginBottom: '1.5rem' }}>
          <button
            type="button"
            className="nav-item"
            style={{
              flex: 1,
              textAlign: 'center',
              borderBottom: mode === 'login' ? '2px solid var(--accent-primary)' : 'none',
              borderRadius: 0,
              color: mode === 'login' ? '#fff' : 'var(--text-muted)',
              fontWeight: 600,
            }}
            onClick={() => { setMode('login'); setError(null); setIsNetworkError(false); }}
          >
            Sign In
          </button>
          <button
            type="button"
            className="nav-item"
            style={{
              flex: 1,
              textAlign: 'center',
              borderBottom: mode === 'register' ? '2px solid var(--accent-primary)' : 'none',
              borderRadius: 0,
              color: mode === 'register' ? '#fff' : 'var(--text-muted)',
              fontWeight: 600,
            }}
            onClick={() => { setMode('register'); setError(null); setIsNetworkError(false); }}
          >
            Register
          </button>
        </div>

        {error && (
          <div className="alert-box alert-danger" role="alert" style={{ marginBottom: '1rem' }}>
            <span>⚠️ {error}</span>
          </div>
        )}

        {isNetworkError && (
          <div style={{
            marginBottom: '1.25rem',
            padding: '0.85rem',
            background: 'rgba(0,0,0,0.3)',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-subtle)'
          }}>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.4rem', fontWeight: 600 }}>
              🌐 Configure Backend API URL:
            </label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="text"
                value={backendUrlInput}
                onChange={(e) => setBackendUrlInput(e.target.value)}
                placeholder="https://your-backend.onrender.com"
                className="select-control"
                style={{ flex: 1, padding: '0.45rem 0.65rem', fontSize: '0.8rem' }}
              />
              <button
                type="button"
                className="btn btn-primary"
                style={{ padding: '0.45rem 0.85rem', fontSize: '0.8rem', whiteSpace: 'nowrap' }}
                onClick={handleSaveBackendUrl}
              >
                Save & Retry
              </button>
            </div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.35rem' }}>
              Paste your live backend URL (e.g. from Render dashboard).
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {mode === 'register' && (
            <div style={{ marginBottom: '1.25rem' }}>
              <label htmlFor="reg-fullname" className="control-group-label">
                Full Name
              </label>
              <input
                id="reg-fullname"
                type="text"
                className="select-control"
                placeholder="e.g. Jane Doe"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
                autoComplete="name"
              />
            </div>
          )}

          <div style={{ marginBottom: '1.25rem' }}>
            <label htmlFor="auth-email" className="control-group-label">
              Email Address
            </label>
            <input
              id="auth-email"
              type="email"
              className="select-control"
              placeholder="user@college.edu"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label htmlFor="auth-password" className="control-group-label">
              Password
            </label>
            <input
              id="auth-password"
              type="password"
              className="select-control"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
              autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%' }}
            disabled={loading}
          >
            {loading ? 'Authenticating...' : mode === 'login' ? 'Sign In' : 'Create Account'}
          </button>

          <div style={{ marginTop: '1.25rem', textAlign: 'center', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Tokens are strictly kept in memory. No credentials saved to localStorage.
          </div>
        </form>
      </div>
    </div>
  );
};

export default AuthModal;
