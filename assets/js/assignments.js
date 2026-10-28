/**
 * EduAdapt-AI - Assignment & Assessment Engine
 * Manages 10-question MCQ quizzes, navigation, score calculation, pass/fail grading (70%),
 * progression unlocking, local storage persistence, and quiz history.
 */

(function () {
    let currentSubjectId = 'python';
    let currentLevel = 'easy';
    let currentQuestions = [];
    let currentQuestionIndex = 0;
    let studentAnswers = {}; // { [qIndex]: selectedOptionIndex }

    document.addEventListener('DOMContentLoaded', () => {
        const user = window.Auth ? window.Auth.requireAuth() : null;
        if (!user) return;

        // Check if on results.html or assignments.html
        if (window.location.pathname.includes('results.html')) {
            initResultsPage();
            return;
        }

        initAssignmentsPage();
    });

    function initAssignmentsPage() {
        const urlParams = new URLSearchParams(window.location.search);
        currentSubjectId = urlParams.get('subject') || 'python';
        currentLevel = (urlParams.get('level') || 'easy').toLowerCase();

        // Setup subject & level selectors
        initSubjectDropdown();
        initLevelTabs();

        // Check JavaScript Level Access
        loadAssessment(currentSubjectId, currentLevel);

        // Render past attempts table
        renderAssessmentHistory();
    }

    function initSubjectDropdown() {
        const dropdown = document.getElementById('assignmentSubjectSelect');
        if (!dropdown) return;

        const catalog = window.SUBJECTS_DATA || {};
        let options = '';
        Object.keys(catalog).forEach(sId => {
            options += `<option value="${sId}" ${sId === currentSubjectId ? 'selected' : ''}>${catalog[sId].title}</option>`;
        });
        dropdown.innerHTML = options;

        dropdown.addEventListener('change', (e) => {
            currentSubjectId = e.target.value;
            loadAssessment(currentSubjectId, currentLevel);
        });
    }

    function initLevelTabs() {
        const container = document.getElementById('assignmentLevelTabs');
        if (!container) return;

        container.querySelectorAll('.quiz-level-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const lvl = btn.getAttribute('data-level');
                currentLevel = lvl;
                loadAssessment(currentSubjectId, currentLevel);
            });
        });
    }

    function updateLevelButtonsUI() {
        document.querySelectorAll('.quiz-level-btn').forEach(btn => {
            const lvl = btn.getAttribute('data-level');
            const isUnlocked = window.App.isLevelUnlocked(currentSubjectId, lvl);
            const isActive = lvl === currentLevel;

            if (isActive) {
                btn.className = 'btn btn-primary active fw-bold quiz-level-btn';
            } else {
                btn.className = `btn ${isUnlocked ? 'btn-outline-secondary' : 'btn-outline-secondary opacity-75'} quiz-level-btn`;
            }

            const lockIcon = btn.querySelector('.lock-indicator');
            if (lockIcon) {
                lockIcon.innerHTML = isUnlocked ? '' : '<i class="bi bi-lock-fill text-warning ms-1"></i>';
            }
        });
    }

    function loadAssessment(subjectId, level) {
        currentSubjectId = subjectId;
        currentLevel = level;
        currentQuestionIndex = 0;
        studentAnswers = {};

        updateLevelButtonsUI();

        const isUnlocked = window.App.isLevelUnlocked(subjectId, level);
        const quizCard = document.getElementById('quizCardContainer');
        const lockedCard = document.getElementById('quizLockedContainer');

        if (!isUnlocked) {
            if (quizCard) quizCard.classList.add('d-none');
            if (lockedCard) {
                lockedCard.classList.remove('d-none');
                const prevLvl = level === 'complex' ? 'medium' : 'easy';
                lockedCard.innerHTML = `
                    <div class="level-locked-banner shadow-sm my-4 text-center">
                        <div class="p-3 text-warning fs-1"><i class="bi bi-shield-lock-fill"></i></div>
                        <h4 class="fw-bold text-dark mb-2">Assessment Locked: ${level.toUpperCase()}</h4>
                        <p class="text-secondary mb-4 mx-auto" style="max-width: 500px;">
                            You must first score <strong>70% or higher</strong> on the <strong>${prevLvl.toUpperCase()}</strong> assessment to unlock this level.
                        </p>
                        <button type="button" class="btn btn-warning fw-bold px-4" onclick="window.location.href='assignments.html?subject=${subjectId}&level=${prevLvl}'">
                            <i class="bi bi-arrow-left-circle me-1"></i> Switch to ${prevLvl.toUpperCase()} Assessment
                        </button>
                    </div>
                `;
            }
            return;
        }

        if (lockedCard) lockedCard.classList.add('d-none');
        if (quizCard) quizCard.classList.remove('d-none');

        const allQuestions = window.ASSIGNMENT_QUESTIONS || {};
        const subjectQuestions = allQuestions[subjectId] || {};
        currentQuestions = subjectQuestions[level] || [];

        if (currentQuestions.length === 0) {
            quizCard.innerHTML = '<div class="alert alert-info">No questions available for this module.</div>';
            return;
        }

        renderQuestionNavigator();
        renderActiveQuestion();
    }

    function renderQuestionNavigator() {
        const container = document.getElementById('quizNavPills');
        if (!container) return;

        let html = '';
        currentQuestions.forEach((q, idx) => {
            const isAnswered = studentAnswers[idx] !== undefined;
            const isCurrent = idx === currentQuestionIndex;

            let badgeClass = 'btn-outline-secondary';
            if (isCurrent) badgeClass = 'btn-primary active';
            else if (isAnswered) badgeClass = 'btn-success text-white';

            html += `
                <button type="button" class="btn btn-sm ${badgeClass} q-pill-btn" data-index="${idx}" style="width: 38px; height: 38px;">
                    ${idx + 1}
                </button>
            `;
        });
        container.innerHTML = html;

        container.querySelectorAll('.q-pill-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                currentQuestionIndex = parseInt(btn.getAttribute('data-index'), 10);
                renderQuestionNavigator();
                renderActiveQuestion();
            });
        });
    }

    function renderActiveQuestion() {
        const q = currentQuestions[currentQuestionIndex];
        if (!q) return;

        // Progress Text & Bar
        const progressTextEl = document.getElementById('quizQuestionCounter');
        if (progressTextEl) {
            progressTextEl.textContent = `Question ${currentQuestionIndex + 1} of ${currentQuestions.length}`;
        }

        const progressBarEl = document.getElementById('quizProgressBar');
        if (progressBarEl) {
            const pct = Math.round(((currentQuestionIndex + 1) / currentQuestions.length) * 100);
            progressBarEl.style.width = `${pct}%`;
        }

        // Subject & Level Badge
        const metaEl = document.getElementById('quizMetaBadges');
        const catalog = window.SUBJECTS_DATA || {};
        const subject = catalog[currentSubjectId];
        if (metaEl && subject) {
            metaEl.innerHTML = `
                <span class="badge bg-${subject.badge_color || 'primary'}-subtle text-${subject.badge_color || 'primary'} border text-uppercase">${subject.title}</span>
                <span class="badge bg-light text-dark border text-capitalize">${currentLevel} Level</span>
                <span class="badge bg-warning-subtle text-warning border">Pass Threshold: 70%</span>
            `;
        }

        // Question Title
        const textEl = document.getElementById('quizQuestionText');
        if (textEl) textEl.textContent = q.question;

        // Render 4 Options
        const optionsContainer = document.getElementById('quizOptionsContainer');
        if (optionsContainer) {
            const letters = ['A', 'B', 'C', 'D'];
            let html = '';
            q.options.forEach((optText, optIdx) => {
                const isChecked = studentAnswers[currentQuestionIndex] === optIdx;
                html += `
                    <div class="mb-2">
                        <input type="radio" name="assessment_opt" class="option-input" id="opt_${optIdx}" value="${optIdx}" ${isChecked ? 'checked' : ''}>
                        <label for="opt_${optIdx}" class="option-label">
                            <span class="option-indicator">${letters[optIdx]}</span>
                            <span class="fw-medium text-dark">${optText}</span>
                        </label>
                    </div>
                `;
            });
            optionsContainer.innerHTML = html;

            // Option selection listener
            optionsContainer.querySelectorAll('input[name="assessment_opt"]').forEach(input => {
                input.addEventListener('change', (e) => {
                    studentAnswers[currentQuestionIndex] = parseInt(e.target.value, 10);
                    renderQuestionNavigator();
                    updateNavButtons();
                });
            });
        }

        updateNavButtons();
    }

    function updateNavButtons() {
        const prevBtn = document.getElementById('quizPrevBtn');
        const nextBtn = document.getElementById('quizNextBtn');
        const submitBtn = document.getElementById('quizSubmitBtn');

        if (prevBtn) {
            prevBtn.disabled = currentQuestionIndex === 0;
            prevBtn.onclick = () => {
                if (currentQuestionIndex > 0) {
                    currentQuestionIndex--;
                    renderQuestionNavigator();
                    renderActiveQuestion();
                }
            };
        }

        const isLastQuestion = currentQuestionIndex === currentQuestions.length - 1;
        if (nextBtn) {
            nextBtn.classList.toggle('d-none', isLastQuestion);
            nextBtn.onclick = () => {
                if (currentQuestionIndex < currentQuestions.length - 1) {
                    currentQuestionIndex++;
                    renderQuestionNavigator();
                    renderActiveQuestion();
                }
            };
        }

        if (submitBtn) {
            submitBtn.classList.toggle('d-none', !isLastQuestion);
            submitBtn.onclick = submitAssessment;
        }
    }

    function submitAssessment() {
        const answeredCount = Object.keys(studentAnswers).length;
        const total = currentQuestions.length;

        if (answeredCount < total) {
            const unanswered = total - answeredCount;
            if (!confirm(`You have ${unanswered} unanswered question(s). Are you sure you want to submit?`)) {
                return;
            }
        }

        // Calculate score
        let score = 0;
        const detailedAnswers = [];

        currentQuestions.forEach((q, idx) => {
            const chosen = studentAnswers[idx] !== undefined ? studentAnswers[idx] : null;
            const isCorrect = chosen === q.correct_index;
            if (isCorrect) score++;

            detailedAnswers.push({
                questionId: q.id,
                question: q.question,
                options: q.options,
                selectedIndex: chosen,
                correctIndex: q.correct_index,
                isCorrect: isCorrect,
                explanation: q.explanation
            });
        });

        const percentage = Math.round((score / total) * 100);
        const passed = percentage >= 70;

        const attemptData = {
            subjectId: currentSubjectId,
            level: currentLevel,
            score: score,
            total: total,
            percentage: percentage,
            passed: passed,
            answers: detailedAnswers
        };

        const result = window.App.recordAssignmentAttempt(attemptData);

        // Store latest attempt for results page
        sessionStorage.setItem('eduadapt_latest_attempt', JSON.stringify(result.attempt));

        // Redirect to results page
        window.location.href = `results.html?attemptId=${result.attempt.id}&unlocked=${result.unlockedLevel || ''}`;
    }

    function renderAssessmentHistory() {
        const tableBody = document.getElementById('assessmentHistoryTableBody');
        const emptyAlert = document.getElementById('noHistoryAlert');
        if (!tableBody) return;

        const history = window.App.getAssignmentHistory();
        const catalog = window.SUBJECTS_DATA || {};

        if (history.length === 0) {
            tableBody.innerHTML = '';
            if (emptyAlert) emptyAlert.classList.remove('d-none');
            return;
        }

        if (emptyAlert) emptyAlert.classList.add('d-none');
        let html = '';

        history.forEach(att => {
            const subj = catalog[att.subjectId];
            const title = subj ? subj.title : att.subjectId;
            const dateStr = new Date(att.timestamp).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
            const badge = att.passed
                ? '<span class="badge bg-success-subtle text-success border border-success"><i class="bi bi-check-circle-fill me-1"></i> Passed (≥70%)</span>'
                : '<span class="badge bg-danger-subtle text-danger border border-danger"><i class="bi bi-x-circle-fill me-1"></i> Failed (<70%)</span>';

            html += `
            <tr>
                <td class="fw-semibold">${title}</td>
                <td><span class="badge bg-light text-dark text-capitalize border">${att.level}</span></td>
                <td><span class="fw-bold ${att.passed ? 'text-success' : 'text-danger'}">${att.score} / ${att.total}</span></td>
                <td>${att.percentage}%</td>
                <td>${badge}</td>
                <td class="small text-muted">${dateStr}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary review-attempt-btn" data-attempt-id="${att.id}">
                        Review
                    </button>
                    <a href="assignments.html?subject=${att.subjectId}&level=${att.level}" class="btn btn-sm btn-outline-secondary ms-1">
                        Retry
                    </a>
                </td>
            </tr>
            `;
        });

        tableBody.innerHTML = html;

        tableBody.querySelectorAll('.review-attempt-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const attId = btn.getAttribute('data-attempt-id');
                const target = history.find(h => h.id === attId);
                if (target) {
                    sessionStorage.setItem('eduadapt_latest_attempt', JSON.stringify(target));
                    window.location.href = `results.html?attemptId=${attId}`;
                }
            });
        });
    }

    // --- Results Page Controller ---
    function initResultsPage() {
        const urlParams = new URLSearchParams(window.location.search);
        const attemptId = urlParams.get('attemptId');
        const unlocked = urlParams.get('unlocked');

        let attempt = null;
        try {
            const sessionData = sessionStorage.getItem('eduadapt_latest_attempt');
            if (sessionData) {
                const parsed = JSON.parse(sessionData);
                if (!attemptId || parsed.id === attemptId) {
                    attempt = parsed;
                }
            }
        } catch (e) {
            console.error('Session attempt parse error', e);
        }

        if (!attempt) {
            const history = window.App.getAssignmentHistory();
            attempt = history.find(h => h.id === attemptId) || history[0];
        }

        if (!attempt) {
            window.location.href = 'assignments.html';
            return;
        }

        renderResultSummary(attempt, unlocked);
        renderQuestionsReview(attempt);
    }

    function renderResultSummary(attempt, unlocked) {
        const catalog = window.SUBJECTS_DATA || {};
        const subject = catalog[attempt.subjectId];
        const subTitle = subject ? subject.title : attempt.subjectId;

        // Subject & Level
        const subHeader = document.getElementById('resultSubjectTitle');
        if (subHeader) subHeader.textContent = `${subTitle} – ${attempt.level.toUpperCase()} Assessment`;

        // Percentage & Score Badge
        const scoreBadge = document.getElementById('resultScoreDisplay');
        if (scoreBadge) {
            scoreBadge.innerHTML = `
                <div class="display-3 fw-bold ${attempt.passed ? 'text-success' : 'text-danger'}">${attempt.percentage}%</div>
                <div class="fs-5 text-muted">${attempt.score} out of ${attempt.total} Questions Correct</div>
            `;
        }

        // Pass/Fail Banner
        const bannerEl = document.getElementById('resultStatusBanner');
        if (bannerEl) {
            if (attempt.passed) {
                bannerEl.className = 'alert alert-success border-0 shadow-sm p-4 rounded-3 text-center mb-4';
                bannerEl.innerHTML = `
                    <div class="fs-1 text-success mb-2"><i class="bi bi-trophy-fill"></i></div>
                    <h3 class="fw-bold mb-1">Congratulations! You Passed!</h3>
                    <p class="mb-0">You scored <strong>${attempt.percentage}%</strong>, surpassing the 70% threshold.</p>
                `;
            } else {
                bannerEl.className = 'alert alert-danger border-0 shadow-sm p-4 rounded-3 text-center mb-4';
                bannerEl.innerHTML = `
                    <div class="fs-1 text-danger mb-2"><i class="bi bi-exclamation-octagon-fill"></i></div>
                    <h3 class="fw-bold mb-1">Assessment Needs Improvement</h3>
                    <p class="mb-0">You scored <strong>${attempt.percentage}%</strong>. The passing threshold is <strong>70%</strong>. Review the study concepts below and retry!</p>
                `;
            }
        }

        // Unlocked Level Alert
        const unlockAlert = document.getElementById('resultUnlockAlert');
        if (unlockAlert) {
            if (unlocked === 'mastered') {
                unlockAlert.classList.remove('d-none');
                unlockAlert.innerHTML = `
                    <div class="alert alert-primary border-0 shadow-sm p-3 d-flex align-items-center gap-3">
                        <i class="bi bi-patch-check-fill fs-2 text-primary"></i>
                        <div>
                            <strong class="d-block">Mastery Achieved! 🎓</strong>
                            <span>You have mastered all three levels of <strong>${subTitle}</strong>. Exceptional work!</span>
                        </div>
                    </div>
                `;
            } else if (unlocked) {
                unlockAlert.classList.remove('d-none');
                unlockAlert.innerHTML = `
                    <div class="alert alert-success border-0 shadow-sm p-3 d-flex align-items-center gap-3">
                        <i class="bi bi-unlock-fill fs-2 text-success"></i>
                        <div>
                            <strong class="d-block">New Level Unlocked! 🎉</strong>
                            <span>Level <strong>${unlocked.toUpperCase()}</strong> is now unlocked in your curriculum.</span>
                        </div>
                    </div>
                `;
            } else {
                unlockAlert.classList.add('d-none');
            }
        }

        // Action Buttons
        const retryBtn = document.getElementById('resultRetryBtn');
        if (retryBtn) {
            retryBtn.href = `assignments.html?subject=${attempt.subjectId}&level=${attempt.level}`;
        }

        const studyBtn = document.getElementById('resultStudyBtn');
        if (studyBtn) {
            studyBtn.href = `study-material.html?subject=${attempt.subjectId}&level=${attempt.level}`;
        }
    }

    function renderQuestionsReview(attempt) {
        const container = document.getElementById('resultQuestionsReviewContainer');
        if (!container) return;

        const answers = attempt.answers || [];
        const letters = ['A', 'B', 'C', 'D'];
        let html = '';

        answers.forEach((item, idx) => {
            const isCorrect = item.isCorrect;
            const statusBadge = isCorrect
                ? '<span class="badge bg-success-subtle text-success border border-success"><i class="bi bi-check-lg me-1"></i> Correct</span>'
                : '<span class="badge bg-danger-subtle text-danger border border-danger"><i class="bi bi-x-lg me-1"></i> Incorrect</span>';

            let optionsHtml = '';
            item.options.forEach((optText, optIdx) => {
                const isSelected = item.selectedIndex === optIdx;
                const isCorrectOpt = item.correctIndex === optIdx;

                let optClass = 'result-option';
                let icon = '';

                if (isCorrectOpt) {
                    optClass += ' result-option-correct';
                    icon = '<i class="bi bi-check-circle-fill text-success me-2"></i>';
                } else if (isSelected && !isCorrect) {
                    optClass += ' result-option-wrong';
                    icon = '<i class="bi bi-x-circle-fill text-danger me-2"></i>';
                }

                optionsHtml += `
                    <div class="${optClass} d-flex align-items-center">
                        <span class="fw-bold me-2" style="width: 24px;">${letters[optIdx]}.</span>
                        <span class="flex-grow-1">${optText}</span>
                        ${icon}
                        ${isSelected ? '<span class="badge bg-secondary ms-2" style="font-size:0.65rem;">Your Choice</span>' : ''}
                    </div>
                `;
            });

            html += `
            <div class="card mb-4 border-0 shadow-sm p-4 rounded-3">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="badge bg-light text-dark border">Question ${idx + 1} of ${answers.length}</span>
                    ${statusBadge}
                </div>
                <h5 class="fw-bold text-dark mb-3">${item.question}</h5>
                
                <div class="mb-3">
                    ${optionsHtml}
                </div>

                <div class="p-3 bg-light rounded-3 border-start border-4 border-info">
                    <strong class="d-block small text-info mb-1"><i class="bi bi-lightbulb-fill me-1"></i> Pedagogical Explanation:</strong>
                    <div class="small text-secondary">${item.explanation}</div>
                </div>
            </div>
            `;
        });

        container.innerHTML = html;
    }

    window.Assessment = {
        loadAssessment,
        submitAssessment
    };
})();
