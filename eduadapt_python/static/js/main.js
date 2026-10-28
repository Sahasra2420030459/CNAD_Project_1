/**
 * EduAdapt-AI Main Client Script
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Code Copy Buttons
    document.querySelectorAll('.code-copy-btn').forEach(button => {
        button.addEventListener('click', () => {
            const container = button.closest('.code-container');
            if (!container) return;
            const codeEl = container.querySelector('.code-content');
            if (!codeEl) return;

            navigator.clipboard.writeText(codeEl.innerText).then(() => {
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="bi bi-check-lg text-success"></i> Copied!';
                setTimeout(() => {
                    button.innerHTML = originalText;
                }, 2000);
            }).catch(err => {
                console.error('Clipboard copy failed:', err);
            });
        });
    });

    // 2. Topic Search Filter in Learning Sidebar
    const topicSearchInput = document.getElementById('topicSearchInput');
    if (topicSearchInput) {
        topicSearchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            document.querySelectorAll('.topic-nav-item').forEach(item => {
                const text = item.innerText.toLowerCase();
                if (text.includes(query)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // 3. Mark Topic Completed via AJAX
    const markCompleteBtn = document.getElementById('markTopicCompleteBtn');
    if (markCompleteBtn) {
        markCompleteBtn.addEventListener('click', async () => {
            const subjectId = markCompleteBtn.dataset.subjectId;
            const level = markCompleteBtn.dataset.level;
            const topicId = markCompleteBtn.dataset.topicId;

            try {
                const res = await fetch('/api/topic/complete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ subject_id: subjectId, level: level, topic_id: topicId })
                });
                const data = await res.json();
                if (data.success) {
                    markCompleteBtn.classList.remove('btn-outline-success');
                    markCompleteBtn.classList.add('btn-success');
                    markCompleteBtn.innerHTML = '<i class="bi bi-check-circle-fill"></i> Completed';
                    markCompleteBtn.disabled = true;

                    // Update corresponding sidebar checkmark
                    const badge = document.getElementById(`badge-${topicId}`);
                    if (badge) {
                        badge.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i>';
                    }
                }
            } catch (err) {
                console.error('Error completing topic:', err);
            }
        });
    }

    // 4. Reveal Practice Question Answer
    document.querySelectorAll('.reveal-answer-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.dataset.target;
            const targetEl = document.getElementById(targetId);
            if (targetEl) {
                if (targetEl.style.display === 'none' || !targetEl.style.display) {
                    targetEl.style.display = 'block';
                    btn.innerHTML = '<i class="bi bi-eye-slash"></i> Hide Explanation';
                } else {
                    targetEl.style.display = 'none';
                    btn.innerHTML = '<i class="bi bi-eye"></i> Reveal Solution';
                }
            }
        });
    });

    // 5. Assessment Progress Tracker
    const assessmentForm = document.getElementById('assessmentForm');
    if (assessmentForm) {
        const totalQuestions = parseInt(assessmentForm.dataset.totalQuestions, 10);
        const progressBar = document.getElementById('assessmentProgressBar');
        const answeredCounter = document.getElementById('answeredCounter');

        const updateProgress = () => {
            const answeredNames = new Set();
            assessmentForm.querySelectorAll('input[type="radio"]:checked').forEach(r => {
                answeredNames.add(r.name);
            });
            const answeredCount = answeredNames.size;
            const pct = Math.round((answeredCount / totalQuestions) * 100);

            if (progressBar) progressBar.style.width = `${pct}%`;
            if (answeredCounter) answeredCounter.innerText = `${answeredCount} of ${totalQuestions} Answered`;
        };

        assessmentForm.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.addEventListener('change', updateProgress);
        });

        // Warn before submitting if unanswered questions remain
        assessmentForm.addEventListener('submit', (e) => {
            const answeredNames = new Set();
            assessmentForm.querySelectorAll('input[type="radio"]:checked').forEach(r => {
                answeredNames.add(r.name);
            });
            if (answeredNames.size < totalQuestions) {
                const unanswered = totalQuestions - answeredNames.size;
                const confirmSubmit = confirm(`You have ${unanswered} unanswered question(s). Are you sure you want to submit your assessment?`);
                if (!confirmSubmit) {
                    e.preventDefault();
                }
            }
        });
    }

    // 6. Auto-dismiss flash alerts after 6 seconds
    setTimeout(() => {
        document.querySelectorAll('.alert-dismissible').forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 6000);
});
