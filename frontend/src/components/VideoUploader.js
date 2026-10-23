import React, { useState, useRef } from 'react';
import { videoApi } from '../services/api';

const ALLOWED_EXTENSIONS = ['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv', 'm4v'];
const MAX_FILE_SIZE = 500 * 1024 * 1024; // 500MB

const PRESETS = [
  {
    id: 'LOW',
    title: 'Low Compression',
    resolution: '1080p (Full HD)',
    crf: 'CRF 22',
    desc: 'High visual fidelity, ideal for presentations and tutorials',
    estimatedReduction: '~25% size reduction',
  },
  {
    id: 'MEDIUM',
    title: 'Medium (Balanced)',
    resolution: '720p (HD)',
    crf: 'CRF 28',
    desc: 'Optimal balance of sharpness and file size for web streaming',
    estimatedReduction: '~50% size reduction',
  },
  {
    id: 'HIGH',
    title: 'High Compression',
    resolution: '480p (SD)',
    crf: 'CRF 32',
    desc: 'Maximum storage efficiency, fast distribution on slow networks',
    estimatedReduction: '~65% size reduction',
  },
];

const TARGET_FORMATS = [
  { id: 'mp4', label: 'MP4 (H.264 + AAC - Universal Compatibility)' },
  { id: 'webm', label: 'WebM (VP9 + Opus - Modern Web Streaming)' },
  { id: 'mkv', label: 'MKV (Matroska - Multi-stream Archival)' },
];

const formatBytes = (bytes) => {
  if (!bytes || bytes <= 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${units[i]}`;
};

const VideoUploader = ({ onUploadSuccess }) => {
  const [stagedFiles, setStagedFiles] = useState([]);
  const [preset, setPreset] = useState('MEDIUM');
  const [targetFormat, setTargetFormat] = useState('mp4');
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [errorMessage, setErrorMessage] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const fileInputRef = useRef(null);

  const validateAndAddFiles = (incomingList) => {
    setErrorMessage(null);
    setSuccessMessage(null);
    const validBatch = [];
    const errorList = [];

    Array.from(incomingList).forEach((file) => {
      // Check duplicate in staged files
      if (stagedFiles.some((f) => f.name === file.name && f.size === file.size)) {
        errorList.push(`"${file.name}" is already staged.`);
        return;
      }

      // Check extension
      const ext = file.name.split('.').pop()?.toLowerCase();
      if (!ext || !ALLOWED_EXTENSIONS.includes(ext)) {
        errorList.push(`"${file.name}": Unsupported format. Allowed: ${ALLOWED_EXTENSIONS.join(', ')}`);
        return;
      }

      // Check max size
      if (file.size > MAX_FILE_SIZE) {
        errorList.push(`"${file.name}": Exceeds 500MB maximum limit (${formatBytes(file.size)})`);
        return;
      }

      // Check empty file
      if (file.size === 0) {
        errorList.push(`"${file.name}": File is empty (0 bytes)`);
        return;
      }

      validBatch.push(file);
    });

    if (errorList.length > 0) {
      setErrorMessage(errorList.join(' | '));
    }

    if (validBatch.length > 0) {
      setStagedFiles((prev) => [...prev, ...validBatch]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndAddFiles(e.dataTransfer.files);
    }
  };

  const removeStagedFile = (indexToRemove) => {
    setStagedFiles((prev) => prev.filter((_, idx) => idx !== indexToRemove));
  };

  const clearAllStaged = () => {
    setStagedFiles([]);
    setErrorMessage(null);
  };

  const totalStagedBytes = stagedFiles.reduce((acc, curr) => acc + curr.size, 0);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (stagedFiles.length === 0) return;

    setUploading(true);
    setUploadProgress(0);
    setErrorMessage(null);
    setSuccessMessage(null);

    const onProgress = (progressEvent) => {
      if (progressEvent.total) {
        const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setUploadProgress(percent);
      }
    };

    try {
      if (stagedFiles.length === 1) {
        await videoApi.uploadSingle(stagedFiles[0], preset, targetFormat, onProgress);
        setSuccessMessage(`Successfully queued "${stagedFiles[0].name}" for asynchronous FFmpeg compression!`);
      } else {
        const batchRes = await videoApi.uploadBatch(stagedFiles, preset, targetFormat, onProgress);
        setSuccessMessage(`Batch processing initialized: ${batchRes.successfulJobs.length} video(s) queued into the transcode pipeline.`);
        if (batchRes.failedFiles && batchRes.failedFiles.length > 0) {
          setErrorMessage(`Failed to enqueue: ${batchRes.failedFiles.map((f) => f.fileName).join(', ')}`);
        }
      }

      setStagedFiles([]);
      setUploadProgress(0);
      if (onUploadSuccess) onUploadSuccess();
    } catch (err) {
      const errDetail = err.response?.data?.message || err.response?.data?.details?.[0] || err.message || 'Upload failed.';
      setErrorMessage(errDetail);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card-panel">
      <div className="panel-header">
        <div>
          <h2 className="panel-title">Video Ingestion & Batch Setup</h2>
          <p className="panel-subtitle">
            Drag-and-drop single or multiple videos to transcode asynchronously via worker nodes.
          </p>
        </div>
      </div>

      {errorMessage && (
        <div className="alert-box alert-danger" role="alert">
          <span>⚠️ {errorMessage}</span>
          <button
            type="button"
            className="logout-icon-btn"
            onClick={() => setErrorMessage(null)}
            aria-label="Dismiss error"
          >
            &times;
          </button>
        </div>
      )}

      {successMessage && (
        <div className="alert-box alert-success" role="status">
          <span>✓ {successMessage}</span>
          <button
            type="button"
            className="logout-icon-btn"
            onClick={() => setSuccessMessage(null)}
            aria-label="Dismiss success message"
          >
            &times;
          </button>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Dropzone */}
        <div
          className={`dropzone-container ${isDragging ? 'is-dragging' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current && fileInputRef.current.click()}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              fileInputRef.current && fileInputRef.current.click();
            }
          }}
          aria-label="Upload files drop area"
        >
          <div className="dropzone-icon-box" aria-hidden="true">
            📥
          </div>
          <div className="dropzone-main-text">
            Drag & drop video files here, or click to browse
          </div>
          <div className="dropzone-sub-text">
            Supports MP4, AVI, MOV, MKV, WebM, FLV (Up to 500MB per file)
          </div>
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            multiple
            accept="video/*,.mkv,.avi,.mov,.webm"
            onChange={(e) => {
              if (e.target.files) validateAndAddFiles(e.target.files);
            }}
          />
        </div>

        {/* Video details before submission */}
        {stagedFiles.length > 0 && (
          <div className="staged-section">
            <div className="staged-header">
              <span className="control-group-label" style={{ margin: 0 }}>
                Staged Videos ({stagedFiles.length})
              </span>
              <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
                <span className="staged-count-badge">Total: {formatBytes(totalStagedBytes)}</span>
                <button
                  type="button"
                  className="btn btn-outline btn-xs"
                  onClick={clearAllStaged}
                  disabled={uploading}
                >
                  Clear All
                </button>
              </div>
            </div>

            <div className="staged-cards-list">
              {stagedFiles.map((file, idx) => (
                <div key={idx} className="staged-card">
                  <div className="video-file-icon" aria-hidden="true">🎬</div>
                  <div className="staged-meta">
                    <div className="staged-filename" title={file.name}>
                      {file.name}
                    </div>
                    <div className="staged-size">
                      {formatBytes(file.size)} • {file.name.split('.').pop()?.toUpperCase()}
                    </div>
                  </div>
                  {!uploading && (
                    <button
                      type="button"
                      className="btn-remove-staged"
                      onClick={() => removeStagedFile(idx)}
                      title="Remove file"
                      aria-label={`Remove ${file.name}`}
                    >
                      &times;
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Compression Settings: Presets and Target Format */}
        <div className="settings-grid-options">
          <div>
            <label className="control-group-label">Compression Preset & Resolution</label>
            <div className="presets-selector-grid" role="radiogroup" aria-label="Compression Presets">
              {PRESETS.map((p) => (
                <div
                  key={p.id}
                  className={`preset-card-option ${preset === p.id ? 'is-selected' : ''}`}
                  onClick={() => setPreset(p.id)}
                  role="radio"
                  aria-checked={preset === p.id}
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      setPreset(p.id);
                    }
                  }}
                >
                  <div className="preset-name">
                    <span>{p.title}</span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--accent-cyan)' }}>{p.crf}</span>
                  </div>
                  <div className="preset-sub" style={{ color: '#fff', fontWeight: 600 }}>
                    {p.resolution}
                  </div>
                  <div className="preset-sub">{p.desc}</div>
                  <div className="preset-sub" style={{ color: 'var(--accent-emerald)', marginTop: '0.35rem' }}>
                    {p.estimatedReduction}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <label htmlFor="target-format-select" className="control-group-label">
              Target Container Format
            </label>
            <select
              id="target-format-select"
              className="select-control"
              value={targetFormat}
              onChange={(e) => setTargetFormat(e.target.value)}
            >
              {TARGET_FORMATS.map((fmt) => (
                <option key={fmt.id} value={fmt.id}>
                  {fmt.label}
                </option>
              ))}
            </select>

            <div style={{ marginTop: '1rem', padding: '0.85rem', background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)' }}>
              <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--accent-cyan)' }}>
                Hardware Acceleration
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                Workers run on OpenJDK 21 + FFmpeg libx264 with multi-threaded thread pools.
              </div>
            </div>
          </div>
        </div>

        {/* Upload Progress Indicator */}
        {uploading && (
          <div style={{ marginTop: '1.5rem' }}>
            <div className="table-progress-bar" style={{ width: '100%', height: '8px' }}>
              <div
                className="table-progress-fill completed"
                style={{ width: `${uploadProgress}%`, transition: 'width 0.2s' }}
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.35rem' }}>
              <span>Streaming files to cloud storage adapter...</span>
              <span>{uploadProgress}%</span>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div style={{ marginTop: '1.75rem', display: 'flex', justifyContent: 'flex-end', gap: '1rem' }}>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={stagedFiles.length === 0 || uploading}
            style={{ minWidth: '220px' }}
          >
            {uploading ? (
              <span>Uploading Batch ({uploadProgress}%)...</span>
            ) : (
              <span>
                🚀 Enqueue {stagedFiles.length > 0 ? `${stagedFiles.length} Video(s)` : 'Videos'}
              </span>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default VideoUploader;
