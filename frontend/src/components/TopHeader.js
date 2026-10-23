import React from 'react';
import { useAuth } from '../context/AuthContext';

const VIEW_TITLES = {
  dashboard: { title: 'Dashboard Overview', desc: 'Real-time asynchronous batch video compression analytics' },
  upload: { title: 'Upload & Transcode', desc: 'Stage videos, select compression presets, and queue async jobs' },
  jobs: { title: 'Active Processing Jobs', desc: 'Live FFmpeg transcoding queue with auto-polling' },
  history: { title: 'Job History & Storage', desc: 'Inspect completed videos, compression metrics, and downloads' },
  settings: { title: 'System Configuration', desc: 'Azure cloud adapters, FFmpeg parameters, and runtime endpoints' },
};

const TopHeader = ({ activeTab, onToggleMobileMenu, onQuickUploadClick }) => {
  const { isAuthenticated } = useAuth();
  const info = VIEW_TITLES[activeTab] || VIEW_TITLES.dashboard;

  return (
    <header className="top-header">
      <div className="header-left">
        <button
          className="menu-toggle-btn"
          onClick={onToggleMobileMenu}
          aria-label="Toggle navigation menu"
        >
          ☰
        </button>
        <div>
          <h1 className="view-heading">{info.title}</h1>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{info.desc}</p>
        </div>
      </div>

      <div className="header-right">
        <div className="system-status-pill" title="Asynchronous worker daemon is healthy">
          <span className="pulse-dot" aria-hidden="true" />
          <span>Worker Pool: Healthy</span>
        </div>

        {isAuthenticated && activeTab !== 'upload' && (
          <button
            className="btn btn-primary btn-xs"
            onClick={onQuickUploadClick}
          >
            + Upload Videos
          </button>
        )}
      </div>
    </header>
  );
};

export default TopHeader;
