import React, { useState, useEffect, useCallback, useRef } from 'react';
import { videoApi } from '../services/api';

const ProcessingJobsTable = ({ initialStatusFilter = 'ALL', onStatsUpdate, title = 'Processing Jobs & Transcoding Queue' }) => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState(initialStatusFilter);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [downloadingId, setDownloadingId] = useState(null);
  const [retryingId, setRetryingId] = useState(null);
  const [selectedErrorJob, setSelectedErrorJob] = useState(null);
  const [tableFeedback, setTableFeedback] = useState(null);

  // Polling control ref
  const pollingTimerRef = useRef(null);

  const fetchJobs = useCallback(async (showLoading = false) => {
    if (showLoading) setLoading(true);
    try {
      const data = await videoApi.getJobs(page, 10, statusFilter);
      const items = data.content || [];
      setJobs(items);
      setTotalPages(data.totalPages || 1);

      // Notify parent to refresh summary stats
      if (onStatsUpdate) onStatsUpdate();

      return items;
    } catch (err) {
      console.error('Failed to fetch processing jobs', err);
      return [];
    } finally {
      if (showLoading) setLoading(false);
    }
  }, [page, statusFilter, onStatsUpdate]);

  // Initial fetch on mount or filter change
  useEffect(() => {
    fetchJobs(true);
  }, [fetchJobs]);

  // Sync status filter if changed from outside (e.g. summary card click)
  useEffect(() => {
    setStatusFilter(initialStatusFilter);
    setPage(0);
  }, [initialStatusFilter]);

  // SMART POLLING: Polls every 3 seconds while QUEUED or PROCESSING jobs exist,
  // and STOPS POLLING completely when all jobs reach terminal states (COMPLETED / FAILED).
  useEffect(() => {
    const hasActiveJobs = jobs.some((j) => j.status === 'QUEUED' || j.status === 'PROCESSING');

    if (hasActiveJobs) {
      pollingTimerRef.current = setInterval(async () => {
        const updatedItems = await fetchJobs(false);
        const stillActive = updatedItems.some((j) => j.status === 'QUEUED' || j.status === 'PROCESSING');
        if (!stillActive && pollingTimerRef.current) {
          clearInterval(pollingTimerRef.current);
          pollingTimerRef.current = null;
        }
      }, 3000);
    } else {
      if (pollingTimerRef.current) {
        clearInterval(pollingTimerRef.current);
        pollingTimerRef.current = null;
      }
    }

    return () => {
      if (pollingTimerRef.current) {
        clearInterval(pollingTimerRef.current);
        pollingTimerRef.current = null;
      }
    };
  }, [jobs, fetchJobs]);

  const handleDownload = async (job) => {
    setDownloadingId(job.id);
    setTableFeedback(null);
    try {
      await videoApi.downloadCompressedVideo(job.id, job.originalFileName);
    } catch (err) {
      const msg = err.response?.data?.message || 'Download failed. Ensure the compressed file is ready.';
      setTableFeedback({ type: 'danger', message: msg });
    } finally {
      setDownloadingId(null);
    }
  };

  const handleRetry = async (job) => {
    setRetryingId(job.id);
    setTableFeedback(null);
    try {
      await videoApi.retryJob(job.id);
      setTableFeedback({ type: 'success', message: `Job #${job.id} re-enqueued into transcode pipeline!` });
      await fetchJobs(false);
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to retry job.';
      setTableFeedback({ type: 'danger', message: msg });
    } finally {
      setRetryingId(null);
    }
  };

  const filteredJobs = jobs.filter((j) => {
    if (!searchTerm) return true;
    return j.originalFileName.toLowerCase().includes(searchTerm.toLowerCase());
  });

  const renderStatusBadge = (status) => {
    switch (status) {
      case 'QUEUED':
        return (
          <span className="status-pill status-QUEUED">
            <span aria-hidden="true">⏳</span> QUEUED
          </span>
        );
      case 'PROCESSING':
        return (
          <span className="status-pill status-PROCESSING">
            <span aria-hidden="true">⚙️</span> PROCESSING
          </span>
        );
      case 'COMPLETED':
        return (
          <span className="status-pill status-COMPLETED">
            <span aria-hidden="true">✓</span> COMPLETED
          </span>
        );
      case 'FAILED':
        return (
          <span className="status-pill status-FAILED">
            <span aria-hidden="true">✕</span> FAILED
          </span>
        );
      default:
        return <span className="status-pill">{status}</span>;
    }
  };

  const renderProgressBar = (status) => {
    if (status === 'COMPLETED') {
      return (
        <div>
          <div className="table-progress-bar">
            <div className="table-progress-fill completed" />
          </div>
          <span style={{ fontSize: '0.7rem', color: 'var(--accent-emerald)', fontWeight: 600 }}>100% Ready</span>
        </div>
      );
    }
    if (status === 'PROCESSING') {
      return (
        <div>
          <div className="table-progress-bar">
            <div className="table-progress-fill processing" />
          </div>
          <span style={{ fontSize: '0.7rem', color: 'var(--accent-cyan)' }}>Transcoding...</span>
        </div>
      );
    }
    if (status === 'QUEUED') {
      return (
        <div>
          <div className="table-progress-bar">
            <div className="table-progress-fill queued" />
          </div>
          <span style={{ fontSize: '0.7rem', color: 'var(--accent-amber)' }}>Waiting in queue</span>
        </div>
      );
    }
    return (
      <span style={{ fontSize: '0.75rem', color: 'var(--accent-rose)', fontWeight: 600 }}>Error halted</span>
    );
  };

  return (
    <div className="card-panel">
      <div className="panel-header">
        <div>
          <h2 className="panel-title">{title}</h2>
          <p className="panel-subtitle">
            Asynchronous background workers continuously ingest and transcode queued videos.
          </p>
        </div>

        {/* Filter & Search Bar */}
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <input
            type="search"
            placeholder="Search filename..."
            className="select-control"
            style={{ width: '180px', padding: '0.45rem 0.75rem', fontSize: '0.85rem' }}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            aria-label="Filter jobs by filename"
          />

          <select
            className="select-control"
            style={{ width: 'auto', padding: '0.45rem 0.85rem', fontSize: '0.85rem' }}
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setPage(0);
            }}
            aria-label="Filter jobs by status"
          >
            <option value="ALL">All Statuses</option>
            <option value="QUEUED">Queued</option>
            <option value="PROCESSING">Processing</option>
            <option value="COMPLETED">Completed</option>
            <option value="FAILED">Failed</option>
          </select>

          <button
            type="button"
            className="btn btn-outline btn-xs"
            onClick={() => fetchJobs(true)}
            title="Refresh jobs list"
            aria-label="Refresh job list"
          >
            ↻ Refresh
          </button>
        </div>
      </div>

      {tableFeedback && (
        <div className={`alert-box alert-${tableFeedback.type}`} role="alert">
          <span>{tableFeedback.message}</span>
          <button
            type="button"
            className="logout-icon-btn"
            onClick={() => setTableFeedback(null)}
            aria-label="Dismiss message"
          >
            &times;
          </button>
        </div>
      )}

      {loading ? (
        <div className="empty-box">
          <div style={{ fontSize: '2rem', animation: 'spin 1s linear infinite', display: 'inline-block' }}>⚙️</div>
          <div className="empty-box-title" style={{ marginTop: '1rem' }}>Loading Jobs...</div>
          <div className="empty-box-desc">Retrieving state machine records from backend database.</div>
        </div>
      ) : filteredJobs.length === 0 ? (
        <div className="empty-box">
          <div className="empty-box-icon">📁</div>
          <div className="empty-box-title">No Video Jobs Found</div>
          <div className="empty-box-desc">
            {searchTerm || statusFilter !== 'ALL'
              ? 'No jobs match your filter criteria. Try resetting the filters.'
              : 'You have not uploaded any videos yet. Navigate to "Upload Videos" to begin!'}
          </div>
        </div>
      ) : (
        <div className="table-responsive-box">
          <table className="data-table" aria-label="Video Processing Jobs">
            <thead>
              <tr>
                <th scope="col">Job ID</th>
                <th scope="col">Video File</th>
                <th scope="col">Status</th>
                <th scope="col">Progress</th>
                <th scope="col">Original</th>
                <th scope="col">Compressed</th>
                <th scope="col">Saved (%)</th>
                <th scope="col">Upload Time</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredJobs.map((job) => (
                <tr key={job.id}>
                  {/* Job ID */}
                  <td>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--accent-cyan)' }}>
                      #{job.id}
                    </span>
                  </td>

                  {/* Filename & Preset */}
                  <td>
                    <div style={{ fontWeight: 600, color: '#fff' }} title={job.originalFileName}>
                      {job.originalFileName}
                    </div>
                    <div style={{ fontSize: '0.725rem', color: 'var(--text-muted)' }}>
                      Preset: {job.preset} ({job.targetResolution || 'Auto'})
                    </div>
                  </td>

                  {/* Status Badge */}
                  <td>{renderStatusBadge(job.status)}</td>

                  {/* Progress Indicator */}
                  <td>{renderProgressBar(job.status)}</td>

                  {/* Original Size */}
                  <td style={{ color: 'var(--text-secondary)' }}>
                    {job.originalSizeFormatted}
                  </td>

                  {/* Compressed Size */}
                  <td>
                    {job.compressedSizeFormatted ? (
                      <span style={{ fontWeight: 600, color: '#fff' }}>{job.compressedSizeFormatted}</span>
                    ) : (
                      <span style={{ color: 'var(--text-muted)' }}>—</span>
                    )}
                  </td>

                  {/* Compression % */}
                  <td>
                    {job.compressionRatioPercent != null ? (
                      <span style={{ color: 'var(--accent-emerald)', fontWeight: 700 }}>
                        {job.compressionRatioPercent}%
                      </span>
                    ) : (
                      <span style={{ color: 'var(--text-muted)' }}>—</span>
                    )}
                  </td>

                  {/* Upload Time */}
                  <td style={{ fontSize: '0.775rem', color: 'var(--text-muted)' }}>
                    {new Date(job.createdAt).toLocaleString(undefined, {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </td>

                  {/* Actions */}
                  <td>
                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                      {job.status === 'COMPLETED' && (
                        <button
                          type="button"
                          className="btn btn-download btn-xs"
                          onClick={() => handleDownload(job)}
                          disabled={downloadingId === job.id}
                          aria-label={`Download compressed ${job.originalFileName}`}
                        >
                          {downloadingId === job.id ? 'Saving...' : '⬇ Download'}
                        </button>
                      )}

                      {job.status === 'FAILED' && (
                        <>
                          <button
                            type="button"
                            className="btn btn-retry btn-xs"
                            onClick={() => handleRetry(job)}
                            disabled={retryingId === job.id}
                            aria-label={`Retry job ${job.id}`}
                          >
                            {retryingId === job.id ? 'Queuing...' : '↻ Retry'}
                          </button>
                          <button
                            type="button"
                            className="btn btn-outline btn-xs"
                            style={{ color: 'var(--accent-rose)', borderColor: 'rgba(244,63,94,0.3)' }}
                            onClick={() => setSelectedErrorJob(job)}
                            aria-label={`View error for job ${job.id}`}
                          >
                            Error
                          </button>
                        </>
                      )}

                      {(job.status === 'QUEUED' || job.status === 'PROCESSING') && (
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          Processing...
                        </span>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Pagination */}
          {totalPages > 1 && (
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1.5rem', padding: '0 0.5rem' }}>
              <button
                type="button"
                className="btn btn-outline btn-xs"
                disabled={page === 0}
                onClick={() => setPage((p) => Math.max(0, p - 1))}
              >
                ← Previous
              </button>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Page {page + 1} of {totalPages}
              </span>
              <button
                type="button"
                className="btn btn-outline btn-xs"
                disabled={page + 1 >= totalPages}
                onClick={() => setPage((p) => p + 1)}
              >
                Next →
              </button>
            </div>
          )}
        </div>
      )}

      {/* Error Details Modal */}
      {selectedErrorJob && (
        <div
          className="modal-overlay"
          onClick={() => setSelectedErrorJob(null)}
          role="dialog"
          aria-modal="true"
          aria-labelledby="error-modal-title"
        >
          <div className="modal-dialog large" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <h3 id="error-modal-title" style={{ color: 'var(--accent-rose)', fontSize: '1.2rem', fontWeight: 700 }}>
                Transcoding Failure Details (Job #{selectedErrorJob.id})
              </h3>
              <button
                type="button"
                className="btn-remove-staged"
                onClick={() => setSelectedErrorJob(null)}
                aria-label="Close dialog"
                style={{ fontSize: '1.5rem' }}
              >
                &times;
              </button>
            </div>

            <div style={{ marginBottom: '1rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              <strong>Video Target:</strong> {selectedErrorJob.originalFileName} | <strong>Preset:</strong> {selectedErrorJob.preset}
            </div>

            <pre style={{
              background: 'rgba(0,0,0,0.5)',
              padding: '1.25rem',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.8rem',
              fontFamily: 'var(--font-mono)',
              whiteSpace: 'pre-wrap',
              maxHeight: '340px',
              overflowY: 'auto',
              color: '#fca5a5',
              border: '1px solid rgba(244,63,94,0.3)',
            }}>
              {selectedErrorJob.errorMessage || 'No detailed error trace provided by the worker.'}
            </pre>

            <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
              <button
                type="button"
                className="btn btn-retry btn-xs"
                onClick={() => {
                  handleRetry(selectedErrorJob);
                  setSelectedErrorJob(null);
                }}
              >
                ↻ Re-enqueue Job
              </button>
              <button
                type="button"
                className="btn btn-outline btn-xs"
                onClick={() => setSelectedErrorJob(null)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProcessingJobsTable;
