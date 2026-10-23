import React from 'react';
import { useAuth } from '../context/AuthContext';

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: '📊' },
  { id: 'upload', label: 'Upload Videos', icon: '⚡' },
  { id: 'jobs', label: 'Processing Jobs', icon: '⚙️' },
  { id: 'history', label: 'History & Analytics', icon: '📁' },
  { id: 'settings', label: 'System Settings', icon: '🔧' },
];

const Sidebar = ({ activeTab, onSelectTab, isOpen, onCloseMobile, onOpenAuth }) => {
  const { user, isAuthenticated, logout } = useAuth();

  const handleNavClick = (tabId) => {
    onSelectTab(tabId);
    if (onCloseMobile) onCloseMobile();
  };

  return (
    <>
      {isOpen && (
        <div
          className="modal-overlay"
          style={{ zIndex: 99, background: 'rgba(0,0,0,0.6)' }}
          onClick={onCloseMobile}
          aria-hidden="true"
        />
      )}

      <aside className={`sidebar ${isOpen ? 'is-open' : ''}`} aria-label="Main Navigation">
        <div className="sidebar-header">
          <div className="brand-badge" aria-hidden="true">🎬</div>
          <div className="brand-info">
            <span className="brand-name">VideoCloud</span>
            <span className="brand-tagline">Async Transcoder</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          {NAV_ITEMS.map((item) => (
            <button
              key={item.id}
              className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => handleNavClick(item.id)}
              aria-current={activeTab === item.id ? 'page' : undefined}
            >
              <span className="nav-icon" aria-hidden="true">{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          {isAuthenticated ? (
            <div className="user-profile-card">
              <div className="user-avatar-circle" aria-hidden="true">
                {user?.fullName?.charAt(0)?.toUpperCase() || 'U'}
              </div>
              <div className="user-details">
                <div className="user-name" title={user?.fullName || user?.email}>
                  {user?.fullName || user?.email}
                </div>
                <div className="user-role">Student Account</div>
              </div>
              <button
                className="logout-icon-btn"
                onClick={logout}
                title="Sign out of account"
                aria-label="Sign out"
              >
                🚪
              </button>
            </div>
          ) : (
            <button
              className="btn btn-primary btn-full btn-xs"
              onClick={() => onOpenAuth('login')}
            >
              Sign In / Register
            </button>
          )}
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
