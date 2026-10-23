import React, { useState, useEffect, useCallback } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Sidebar from './components/Sidebar';
import TopHeader from './components/TopHeader';
import SummaryCards from './components/SummaryCards';
import VideoUploader from './components/VideoUploader';
import ProcessingJobsTable from './components/ProcessingJobsTable';
import SettingsView from './components/SettingsView';
import AuthModal from './components/AuthModal';
import { videoApi } from './services/api';
import './assets/styles.css';

const MainDashboard = () => {
  const { isAuthenticated } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [authModalMode, setAuthModalMode] = useState('login');
  const [stats, setStats] = useState(null);
  const [tableStatusFilter, setTableStatusFilter] = useState('ALL');

  const fetchStats = useCallback(async () => {
    if (!isAuthenticated) return;
    try {
      const data = await videoApi.getStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load user video statistics', err);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  const handleOpenAuth = (mode = 'login') => {
    setAuthModalMode(mode);
    setAuthModalOpen(true);
  };

  const handleCardClick = (statusKey) => {
    setTableStatusFilter(statusKey);
    setActiveTab('jobs');
  };

  const handleUploadSuccess = () => {
    fetchStats();
    setActiveTab('jobs');
  };

  return (
    <div className="app-layout">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        onSelectTab={(tab) => {
          setActiveTab(tab);
          if (tab === 'jobs') setTableStatusFilter('ALL');
          if (tab === 'history') setTableStatusFilter('COMPLETED');
        }}
        isOpen={mobileMenuOpen}
        onCloseMobile={() => setMobileMenuOpen(false)}
        onOpenAuth={handleOpenAuth}
      />

      {/* Main Content Area */}
      <div className="main-wrapper">
        <TopHeader
          activeTab={activeTab}
          onToggleMobileMenu={() => setMobileMenuOpen((prev) => !prev)}
          onQuickUploadClick={() => setActiveTab('upload')}
        />

        <main className="content-area" id="main-content">
          {isAuthenticated ? (
            <>
              {/* Summary Cards always visible on Dashboard view */}
              {activeTab === 'dashboard' && (
                <>
                  <SummaryCards stats={stats} onCardClick={handleCardClick} />

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '2rem' }}>
                    <VideoUploader onUploadSuccess={handleUploadSuccess} />
                    <ProcessingJobsTable
                      initialStatusFilter="ALL"
                      onStatsUpdate={fetchStats}
                      title="Recent Processing Jobs"
                    />
                  </div>
                </>
              )}

              {/* Dedicated Upload Videos View */}
              {activeTab === 'upload' && (
                <div>
                  <VideoUploader onUploadSuccess={handleUploadSuccess} />
                </div>
              )}

              {/* Dedicated Processing Jobs View */}
              {activeTab === 'jobs' && (
                <div>
                  <SummaryCards stats={stats} onCardClick={handleCardClick} />
                  <ProcessingJobsTable
                    initialStatusFilter={tableStatusFilter}
                    onStatsUpdate={fetchStats}
                    title="Processing Queue & Active Transcoding Jobs"
                  />
                </div>
              )}

              {/* History & Storage View */}
              {activeTab === 'history' && (
                <div>
                  <SummaryCards stats={stats} onCardClick={handleCardClick} />
                  <ProcessingJobsTable
                    initialStatusFilter="COMPLETED"
                    onStatsUpdate={fetchStats}
                    title="Completed Video History & Download Center"
                  />
                </div>
              )}

              {/* System Settings View */}
              {activeTab === 'settings' && <SettingsView />}
            </>
          ) : (
            <div className="card-panel empty-box" style={{ maxWidth: '640px', margin: '4rem auto' }}>
              <div style={{ fontSize: '3.5rem', marginBottom: '1.25rem' }}>🔐</div>
              <h2 className="empty-box-title" style={{ fontSize: '1.5rem', marginBottom: '0.75rem' }}>
                Authentication Required
              </h2>
              <p className="empty-box-desc">
                Sign in or register for a student account to access the asynchronous video compression pipeline, stage batches, and download transcoded media with strict tenant isolation.
              </p>
              <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => handleOpenAuth('login')}
                >
                  Sign In
                </button>
                <button
                  type="button"
                  className="btn btn-outline"
                  onClick={() => handleOpenAuth('register')}
                >
                  Create Account
                </button>
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Authentication Modal */}
      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        initialMode={authModalMode}
      />
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <MainDashboard />
    </AuthProvider>
  );
}

export default App;
