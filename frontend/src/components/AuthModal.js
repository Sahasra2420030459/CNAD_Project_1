import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const AuthModal = ({ isOpen, onClose, initialMode = 'login' }) => {
  const [mode, setMode] = useState(initialMode);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const { login, register } = useAuth();

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (mode === 'login') {
        await login(email, password);
      } else {
        await register(email, password, fullName);
      }
      onClose();
    } catch (err) {
      const msg = err.response?.data?.message || err.response?.data?.details?.[0] || 'Authentication failed. Please verify credentials.';
      setError(msg);
    } finally {
      setLoading(false);
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
            onClick={() => { setMode('login'); setError(null); }}
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
            onClick={() => { setMode('register'); setError(null); }}
          >
            Register
          </button>
        </div>

        {error && (
          <div className="alert-box alert-danger" role="alert">
            <span>⚠️ {error}</span>
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
