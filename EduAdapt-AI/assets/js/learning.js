/**
 * EduAdapt-AI - Study Material & Topic Reader Controller
 * Manages curriculum navigation, level security gating, dynamic topic rendering,
 * search filtering, code copying, and lesson completion status.
 */

document.addEventListener('DOMContentLoaded', () => {
    const user = window.Auth ? window.Auth.requireAuth() : null;
    if (!user) return;

    // Parse URL Parameters
    const urlParams = new URLSearchParams(window.location.search);
    let currentSubjectId = urlParams.get('subject') || 'python';
    let currentLevel = (urlParams.get('level') || 'easy').toLowerCase();
    let currentTopicId = urlParams.get('topic');

    const catalog = window.SUBJECTS_DATA || {};
    if (!catalog[currentSubjectId]) {
        currentSubjectId = 'python';
    }

    // Initialize UI controls
    initSubjectSelector(currentSubjectId, currentLevel);
    initLevelSelector(currentSubjectId, currentLevel);
    initTopicSearch();

    // Load initial curriculum view
    loadCurriculum(currentSubjectId, currentLevel, currentTopicId);
});

// Subject switch dropdown / tabs
function initSubjectSelector(activeSubjectId, activeLevel) {
    const selectEl = document.getElementById('subjectSelectorDropdown');
    if (!selectEl) return;

    const catalog = window.SUBJECTS_DATA || {};
    let options = '';
    Object.keys(catalog).forEach(sId => {
        const s = catalog[sId];
        options += `<option value="${sId}" ${sId === activeSubjectId ? 'selected' : ''}>${s.title}</option>`;
    });
    selectEl.innerHTML = options;

    selectEl.addEventListener('change', (e) => {
        const newSubject = e.target.value;
        window.location.href = `study-material.html?subject=${newSubject}&level=easy`;
    });
}

// Level switcher pills
function initLevelSelector(activeSubjectId, activeLevel) {
    const container = document.getElementById('levelSelectorTabs');
    if (!container) return;

    const levels = ['easy', 'medium', 'complex'];
    const levelsState = window.App.getSubjectLevels(activeSubjectId);

    let html = '';
    levels.forEach(lvl => {
        const isUnlocked = window.App.isLevelUnlocked(activeSubjectId, lvl);
        const isActive = lvl === activeLevel;
        const label = lvl.charAt(0).toUpperCase() + lvl.slice(1);

        html += `
            <button type="button" class="btn btn-sm ${isActive ? 'btn-primary active fw-bold' : (isUnlocked ? 'btn-outline-secondary' : 'btn-outline-secondary opacity-75')} level-tab-btn" 
                    data-level="${lvl}" ${isUnlocked ? '' : 'data-locked="true"'}>
                <i class="bi ${isUnlocked ? (isActive ? 'bi-folder2-open' : 'bi-folder2') : 'bi-lock-fill text-warning'} me-1"></i>
                ${label} ${isUnlocked ? '' : '<span class="badge bg-warning text-dark ms-1" style="font-size:0.65rem;">Locked</span>'}
            </button>
        `;
    });
    container.innerHTML = html;

    container.querySelectorAll('.level-tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const chosenLvl = btn.getAttribute('data-level');
            loadCurriculum(activeSubjectId, chosenLvl);
        });
    });
}

// Search filter in topics sidebar
function initTopicSearch() {
    const searchInput = document.getElementById('topicSearchInput');
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        document.querySelectorAll('.topic-nav-item').forEach(item => {
            const title = item.getAttribute('data-topic-title') || '';
            if (title.toLowerCase().includes(query)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

/**
 * Loads and renders the curriculum view with JavaScript-based level access verification.
 */
function loadCurriculum(subjectId, level, requestedTopicId = null) {
    const catalog = window.SUBJECTS_DATA || {};
    const subject = catalog[subjectId];
    if (!subject) return;

    // Update active level tab buttons
    document.querySelectorAll('.level-tab-btn').forEach(btn => {
        const lvl = btn.getAttribute('data-level');
        if (lvl === level) {
            btn.className = 'btn btn-sm btn-primary active fw-bold level-tab-btn';
        } else {
            const isUnl = window.App.isLevelUnlocked(subjectId, lvl);
            btn.className = `btn btn-sm ${isUnl ? 'btn-outline-secondary' : 'btn-outline-secondary opacity-75'} level-tab-btn`;
        }
    });

    const isUnlocked = window.App.isLevelUnlocked(subjectId, level);
    const lockedCard = document.getElementById('levelLockedOverlay');
    const contentArea = document.getElementById('topicContentDisplayArea');
    const sidebarList = document.getElementById('topicsNavList');

    // JAVASCRIPT ACCESS CHECK: Protect locked levels
    if (!isUnlocked) {
        if (sidebarList) sidebarList.innerHTML = '<div class="p-3 text-muted small text-center"><i class="bi bi-lock-fill text-warning fs-4 d-block mb-2"></i>This level is locked. Complete the previous level assessment to view topics.</div>';
        if (contentArea) contentArea.classList.add('d-none');
        if (lockedCard) {
            lockedCard.classList.remove('d-none');
            const prevLvl = level === 'complex' ? 'medium' : 'easy';
            lockedCard.innerHTML = `
                <div class="level-locked-banner shadow-sm my-4">
                    <div class="p-3 text-warning fs-1"><i class="bi bi-shield-lock-fill"></i></div>
                    <h4 class="fw-bold text-dark mb-2">Level Locked: ${level.toUpperCase()}</h4>
                    <p class="text-secondary mb-4 mx-auto" style="max-width: 500px;">
                        To maintain high educational standards and verify mastery, the <strong>${level.toUpperCase()}</strong> track unlocks only after scoring 
                        <strong>70% or higher</strong> on the <strong>${prevLvl.toUpperCase()}</strong> level assessment.
                    </p>
                    <div class="d-flex justify-content-center gap-3">
                        <a href="assignments.html?subject=${subjectId}&level=${prevLvl}" class="btn btn-warning fw-bold px-4">
                            <i class="bi bi-pencil-square me-1"></i> Take ${prevLvl.toUpperCase()} Assessment
                        </a>
                        <button type="button" class="btn btn-outline-secondary" onclick="loadCurriculum('${subjectId}', '${prevLvl}')">
                            <i class="bi bi-arrow-left me-1"></i> Return to ${prevLvl.toUpperCase()}
                        </button>
                    </div>
                </div>
            `;
        }
        return;
    }

    // If level is unlocked, display content
    if (lockedCard) lockedCard.classList.add('d-none');
    if (contentArea) contentArea.classList.remove('d-none');

    const levelData = subject.levels[level];
    if (!levelData || !levelData.topics || levelData.topics.length === 0) return;

    // Render topics sidebar
    renderSidebarTopics(subjectId, level, levelData.topics, requestedTopicId);
}

function renderSidebarTopics(subjectId, level, topics, requestedTopicId) {
    const listEl = document.getElementById('topicsNavList');
    if (!listEl) return;

    let targetTopicId = requestedTopicId;
    if (!targetTopicId || !topics.some(t => t.id === targetTopicId)) {
        targetTopicId = topics[0].id;
    }

    let html = '';
    topics.forEach((topic, idx) => {
        const isCompleted = window.App.isTopicCompleted(subjectId, level, topic.id);
        const isActive = topic.id === targetTopicId;

        html += `
        <li class="topic-nav-item mb-1" data-topic-title="${topic.title}">
            <a href="javascript:void(0)" class="topic-nav-link ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}" 
               data-topic-id="${topic.id}">
                <div class="d-flex align-items-center gap-2 overflow-hidden">
                    <span class="badge ${isCompleted ? 'bg-success text-white' : 'bg-light text-muted border'}" style="font-size:0.7rem; width:22px; height:22px; display:inline-flex; align-items:center; justify-content:center; border-radius:50%;">
                        ${isCompleted ? '<i class="bi bi-check-lg"></i>' : (idx + 1)}
                    </span>
                    <span class="text-truncate">${topic.title}</span>
                </div>
                <small class="text-muted ms-1">${topic.read_time || '8 min'}</small>
            </a>
        </li>
        `;
    });

    listEl.innerHTML = html;

    // Attach click listeners to sidebar links
    listEl.querySelectorAll('.topic-nav-link').forEach(link => {
        link.addEventListener('click', () => {
            const tId = link.getAttribute('data-topic-id');
            // Update active states
            listEl.querySelectorAll('.topic-nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            renderTopicDetail(subjectId, level, tId);
        });
    });

    // Render the initial selected topic
    renderTopicDetail(subjectId, level, targetTopicId);
}

function renderTopicDetail(subjectId, level, topicId) {
    const catalog = window.SUBJECTS_DATA || {};
    const subject = catalog[subjectId];
    const levelData = subject ? subject.levels[level] : null;
    if (!levelData) return;

    const topics = levelData.topics;
    const topicIndex = topics.findIndex(t => t.id === topicId);
    if (topicIndex === -1) return;

    const topic = topics[topicIndex];
    const prevTopic = topicIndex > 0 ? topics[topicIndex - 1] : null;
    const nextTopic = topicIndex < topics.length - 1 ? topics[topicIndex + 1] : null;

    const isCompleted = window.App.isTopicCompleted(subjectId, level, topic.id);

    // Record as recently studied in localStorage
    window.App.recordRecentTopic(subjectId, level, topic.id, topic.title);

    // Update Floating Chat context if available
    const chatDock = document.getElementById('chatWidgetDock');
    if (chatDock) {
        chatDock.dataset.subjectContext = subjectId;
        chatDock.dataset.levelContext = level;
    }

    // Set Header
    const titleEl = document.getElementById('topicTitle');
    if (titleEl) titleEl.textContent = topic.title;

    const metaBadgeEl = document.getElementById('topicMetaBadges');
    if (metaBadgeEl) {
        metaBadgeEl.innerHTML = `
            <span class="badge bg-${subject.badge_color || 'primary'}-subtle text-${subject.badge_color || 'primary'} border text-uppercase">${subject.title}</span>
            <span class="badge bg-light text-dark border text-capitalize"><i class="bi bi-speedometer2 me-1"></i>${level} Level</span>
            <span class="badge bg-light text-muted border"><i class="bi bi-clock me-1"></i>${topic.read_time || '8 min read'}</span>
        `;
    }

    // Summary & Objectives
    const summaryEl = document.getElementById('topicSummary');
    if (summaryEl) summaryEl.textContent = topic.summary;

    const objContainer = document.getElementById('topicObjectivesBox');
    if (objContainer) {
        const objectives = [
            `Understand the core theoretical foundation of ${topic.title.replace(/^\d+\.\s*/, '')}.`,
            `Analyze correct syntax conventions and memory/execution implications.`,
            `Identify and prevent common real-world bugs and anti-patterns.`
        ];
        objContainer.innerHTML = `
            <div class="card bg-primary-subtle border-0 mb-4 p-3 rounded-3">
                <div class="d-flex align-items-center gap-2 mb-2">
                    <i class="bi bi-bullseye text-primary fs-5"></i>
                    <strong class="text-primary">Learning Objectives</strong>
                </div>
                <ul class="mb-0 small text-dark ps-3">
                    ${objectives.map(o => `<li>${o}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    // Detailed Pedagogical Concept Explanation
    const conceptEl = document.getElementById('topicConceptContent');
    if (conceptEl) {
        // Convert markdown bolding and linebreaks for display
        let formattedConcept = topic.concept
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/`([^`]+)`/g, '<code class="bg-light px-1 text-danger rounded">$1</code>')
            .replace(/\n\n/g, '</p><p class="mb-3">')
            .replace(/\n/g, '<br>');
        conceptEl.innerHTML = `<p class="mb-3">${formattedConcept}</p>`;
    }

    // Formal Syntax Box
    const syntaxBox = document.getElementById('topicSyntaxContainer');
    if (syntaxBox) {
        if (topic.syntax) {
            syntaxBox.classList.remove('d-none');
            const codeEl = syntaxBox.querySelector('.code-content');
            if (codeEl) codeEl.textContent = topic.syntax;
        } else {
            syntaxBox.classList.add('d-none');
        }
    }

    // Practical Code Example Box
    const codeBox = document.getElementById('topicCodeContainer');
    if (codeBox) {
        if (topic.code_example) {
            codeBox.classList.remove('d-none');
            const codeEl = codeBox.querySelector('.code-content');
            if (codeEl) codeEl.textContent = topic.code_example;
        } else {
            codeBox.classList.add('d-none');
        }
    }

    // Expected Output Box
    const outputBox = document.getElementById('topicOutputContainer');
    if (outputBox) {
        if (topic.expected_output) {
            outputBox.classList.remove('d-none');
            const textEl = outputBox.querySelector('.output-box');
            if (textEl) textEl.textContent = topic.expected_output;
        } else {
            outputBox.classList.add('d-none');
        }
    }

    // Common Mistakes Callout
    const mistakesEl = document.getElementById('topicCommonMistakes');
    if (mistakesEl) {
        if (topic.common_mistakes) {
            mistakesEl.classList.remove('d-none');
            let formattedMistakes = topic.common_mistakes
                .replace(/`([^`]+)`/g, '<code class="bg-white px-1 text-danger rounded">$1</code>');
            mistakesEl.innerHTML = `
                <div class="alert alert-warning border-0 shadow-sm d-flex gap-3 mb-4">
                    <i class="bi bi-exclamation-triangle-fill fs-4 text-warning flex-shrink-0"></i>
                    <div>
                        <strong class="d-block mb-1">Common Pitfall & Debugging Tip:</strong>
                        <div class="small">${formattedMistakes}</div>
                    </div>
                </div>
            `;
        } else {
            mistakesEl.classList.add('d-none');
        }
    }

    // Practice Question with Interactive Reveal Solution
    const practiceBox = document.getElementById('topicPracticeQuestionBox');
    if (practiceBox) {
        if (topic.practice_question) {
            practiceBox.classList.remove('d-none');
            const parts = topic.practice_question.split('(Answer:');
            const questionText = parts[0].trim();
            const answerText = parts.length > 1 ? parts[1].replace(/\)$/, '').trim() : 'Solution reviewed in lecture.';

            practiceBox.innerHTML = `
                <div class="card border-0 bg-light shadow-sm p-4 mb-4 rounded-3">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="badge bg-secondary text-uppercase"><i class="bi bi-question-circle me-1"></i> Knowledge Check</span>
                        <button type="button" class="btn btn-sm btn-outline-primary reveal-solution-btn">
                            <i class="bi bi-eye me-1"></i> Reveal Solution
                        </button>
                    </div>
                    <p class="fw-semibold text-dark mb-2">${questionText}</p>
                    <div class="solution-content d-none p-3 mt-2 bg-white rounded border border-success-subtle text-success small">
                        <strong>Correct Answer:</strong> ${answerText}
                    </div>
                </div>
            `;

            const revealBtn = practiceBox.querySelector('.reveal-solution-btn');
            const solutionEl = practiceBox.querySelector('.solution-content');
            revealBtn.addEventListener('click', () => {
                const isHidden = solutionEl.classList.contains('d-none');
                if (isHidden) {
                    solutionEl.classList.remove('d-none');
                    revealBtn.innerHTML = '<i class="bi bi-eye-slash me-1"></i> Hide Solution';
                } else {
                    solutionEl.classList.add('d-none');
                    revealBtn.innerHTML = '<i class="bi bi-eye me-1"></i> Reveal Solution';
                }
            });
        } else {
            practiceBox.classList.add('d-none');
        }
    }

    // Mark as Completed Button
    const completeBtn = document.getElementById('markCompletedBtn');
    if (completeBtn) {
        updateCompletedButtonUI(completeBtn, isCompleted);
        // Replace previous listeners by cloning
        const newCompleteBtn = completeBtn.cloneNode(true);
        completeBtn.parentNode.replaceChild(newCompleteBtn, completeBtn);

        newCompleteBtn.addEventListener('click', () => {
            const newState = window.App.toggleTopicCompletion(subjectId, level, topic.id);
            updateCompletedButtonUI(newCompleteBtn, newState);

            // Update sidebar link icon
            const link = document.querySelector(`.topic-nav-link[data-topic-id="${topic.id}"]`);
            if (link) {
                if (newState) link.classList.add('completed');
                else link.classList.remove('completed');
                const badge = link.querySelector('.badge');
                if (badge) {
                    badge.className = `badge ${newState ? 'bg-success text-white' : 'bg-light text-muted border'}`;
                    badge.innerHTML = newState ? '<i class="bi bi-check-lg"></i>' : (topicIndex + 1);
                }
            }

            if (newState) {
                window.App.showToast(`Completed "<strong>${topic.title}</strong>"! Progress saved.`, 'success');
            } else {
                window.App.showToast(`Marked "<strong>${topic.title}</strong>" as incomplete.`, 'info');
            }
        });
    }

    // Previous & Next Topic Buttons
    const prevBtn = document.getElementById('prevTopicBtn');
    if (prevBtn) {
        if (prevTopic) {
            prevBtn.classList.remove('disabled');
            prevBtn.onclick = () => renderTopicDetail(subjectId, level, prevTopic.id);
        } else {
            prevBtn.classList.add('disabled');
            prevBtn.onclick = null;
        }
    }

    const nextBtn = document.getElementById('nextTopicBtn');
    if (nextBtn) {
        if (nextTopic) {
            nextBtn.classList.remove('disabled');
            nextBtn.onclick = () => renderTopicDetail(subjectId, level, nextTopic.id);
        } else {
            nextBtn.classList.add('disabled');
            nextBtn.onclick = null;
        }
    }

    // Scroll to top of content display
    window.scrollTo({ top: 120, behavior: 'smooth' });

    // Re-bind code copy
    window.App.setupCodeCopy();
}

function updateCompletedButtonUI(btn, isCompleted) {
    if (isCompleted) {
        btn.className = 'btn btn-success btn-sm px-3';
        btn.innerHTML = '<i class="bi bi-check-circle-fill me-1"></i> Completed';
    } else {
        btn.className = 'btn btn-outline-success btn-sm px-3';
        btn.innerHTML = '<i class="bi bi-check-circle me-1"></i> Mark as Completed';
    }
}
