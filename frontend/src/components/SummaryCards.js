import React from 'react';

const SummaryCards = ({ stats, onCardClick }) => {
  const cards = [
    {
      id: 'ALL',
      type: 'card-total',
      label: 'Total Videos',
      value: stats?.totalJobs ?? 0,
      icon: '📹',
      desc: stats?.totalSavedFormatted ? `${stats.totalSavedFormatted} saved` : 'Total ingested',
    },
    {
      id: 'QUEUED',
      type: 'card-queued',
      label: 'Queued',
      value: stats?.queuedJobs ?? 0,
      icon: '⏳',
      desc: 'Awaiting worker node',
    },
    {
      id: 'PROCESSING',
      type: 'card-processing',
      label: 'Processing',
      value: stats?.processingJobs ?? 0,
      icon: '⚙️',
      desc: 'Transcoding with FFmpeg',
    },
    {
      id: 'COMPLETED',
      type: 'card-completed',
      label: 'Completed',
      value: stats?.completedJobs ?? 0,
      icon: '✓',
      desc: stats?.averageCompressionPercent ? `Avg ${stats.averageCompressionPercent}% reduced` : 'Ready to download',
    },
    {
      id: 'FAILED',
      type: 'card-failed',
      label: 'Failed',
      value: stats?.failedJobs ?? 0,
      icon: '✕',
      desc: 'Eligible for retry',
    },
  ];

  return (
    <div className="summary-cards-grid" role="region" aria-label="System Summary Metrics">
      {cards.map((card) => (
        <div
          key={card.id}
          className={`summary-card ${card.type}`}
          onClick={() => onCardClick && onCardClick(card.id)}
          style={{ cursor: onCardClick ? 'pointer' : 'default' }}
          role={onCardClick ? 'button' : undefined}
          tabIndex={onCardClick ? 0 : undefined}
          onKeyDown={(e) => {
            if (onCardClick && (e.key === 'Enter' || e.key === ' ')) {
              e.preventDefault();
              onCardClick(card.id);
            }
          }}
        >
          <div className="summary-header">
            <span className="summary-label">{card.label}</span>
            <span className="summary-icon-pill" aria-hidden="true">{card.icon}</span>
          </div>
          <div className="summary-value">{card.value}</div>
          <div className="summary-footer">{card.desc}</div>
        </div>
      ))}
    </div>
  );
};

export default SummaryCards;
