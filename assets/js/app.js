/**
 * EduAdapt-AI - Core Platform Application & Storage Engine
 * Coordinates local storage state, progression checks, assignments, and cross-component notifications.
 */

(function () {
    const App = {};

    // Helper: active student key prefix
    function getUserKey(prefix) {
        const user = window.Auth ? window.Auth.getCurrentUser() : null;
        const email = user ? user.email.toLowerCase() : 'guest';
        return `eduadapt_${prefix}_${email}`;
    }

    // --- Enrolled Subjects Management ---
    App.getSelectedSubjects = function () {
        try {
            const data = localStorage.getItem(getUserKey('selected_subjects'));
            if (!data) {
                // Default enrollment for quick start
                return ['python', 'dbms'];
            }
            return JSON.parse(data);
        } catch (e) {
            console.error('Error reading selected subjects:', e);
            return ['python', 'dbms'];
        }
    };

    App.setSelectedSubjects = function (subjectsList) {
        // Enforce unique items
        const unique = Array.from(new Set(subjectsList));
        localStorage.setItem(getUserKey('selected_subjects'), JSON.stringify(unique));
        // Ensure levels tracking initialized for each
        const levels = App.getAllLevels();
        unique.forEach(s => {
            if (!levels[s]) {
                levels[s] = { easy: true, medium: false, complex: false, completed: false };
            }
        });
        App.saveAllLevels(levels);
    };

    App.addSubject = function (subjectId) {
        const current = App.getSelectedSubjects();
        if (!current.includes(subjectId)) {
            current.push(subjectId);
            App.setSelectedSubjects(current);
            return true;
        }
        return false;
    };

    App.removeSubject = function (subjectId) {
        const current = App.getSelectedSubjects();
        const filtered = current.filter(id => id !== subjectId);
        App.setSelectedSubjects(filtered);
        return true;
    };

    App.isSubjectSelected = function (subjectId) {
        return App.getSelectedSubjects().includes(subjectId);
    };

    // --- Learning Level Progression Management ---
    App.getAllLevels = function () {
        try {
            const data = localStorage.getItem(getUserKey('levels'));
            if (!data) {
                return {
                    python: { easy: true, medium: false, complex: false, completed: false },
                    java: { easy: true, medium: false, complex: false, completed: false },
                    dbms: { easy: true, medium: false, complex: false, completed: false },
                    dsa: { easy: true, medium: false, complex: false, completed: false }
                };
            }
            return JSON.parse(data);
        } catch (e) {
            return {
                python: { easy: true, medium: false, complex: false, completed: false },
                java: { easy: true, medium: false, complex: false, completed: false },
                dbms: { easy: true, medium: false, complex: false, completed: false },
                dsa: { easy: true, medium: false, complex: false, completed: false }
            };
        }
    };

    App.saveAllLevels = function (levelsObj) {
        localStorage.setItem(getUserKey('levels'), JSON.stringify(levelsObj));
    };

    App.getSubjectLevels = function (subjectId) {
        const all = App.getAllLevels();
        return all[subjectId] || { easy: true, medium: false, complex: false, completed: false };
    };

    /**
     * JavaScript Access Verification: Checks if a student can access a specific subject level.
     * Easy is unlocked initially.
     * Passing Easy with >= 70% unlocks Medium.
     * Passing Medium with >= 70% unlocks Complex.
     */
    App.isLevelUnlocked = function (subjectId, level) {
        const lvl = (level || 'easy').toLowerCase();
        if (lvl === 'easy') return true; // Always unlocked by default

        const levels = App.getSubjectLevels(subjectId);
        return !!levels[lvl];
    };

    App.unlockNextLevel = function (subjectId, currentLevel) {
        const lvl = currentLevel.toLowerCase();
        const all = App.getAllLevels();
        if (!all[subjectId]) {
            all[subjectId] = { easy: true, medium: false, complex: false, completed: false };
        }

        let unlockedLevel = null;
        if (lvl === 'easy') {
            all[subjectId].medium = true;
            unlockedLevel = 'medium';
        } else if (lvl === 'medium') {
            all[subjectId].complex = true;
            unlockedLevel = 'complex';
        } else if (lvl === 'complex') {
            all[subjectId].completed = true;
            unlockedLevel = 'mastered';
        }

        App.saveAllLevels(all);
        return unlockedLevel;
    };

    // --- Topic Completion Tracking ---
    App.getCompletedTopicsMap = function () {
        try {
            const data = localStorage.getItem(getUserKey('completed_topics'));
            return data ? JSON.parse(data) : {};
        } catch (e) {
            return {};
        }
    };

    App.isTopicCompleted = function (subjectId, level, topicId) {
        const map = App.getCompletedTopicsMap();
        return !!(map[subjectId] && map[subjectId][level] && map[subjectId][level].includes(topicId));
    };

    App.toggleTopicCompletion = function (subjectId, level, topicId) {
        const map = App.getCompletedTopicsMap();
        if (!map[subjectId]) map[subjectId] = {};
        if (!map[subjectId][level]) map[subjectId][level] = [];

        const index = map[subjectId][level].indexOf(topicId);
        let completed = false;

        if (index > -1) {
            map[subjectId][level].splice(index, 1);
            completed = false;
        } else {
            map[subjectId][level].push(topicId);
            completed = true;
        }

        localStorage.setItem(getUserKey('completed_topics'), JSON.stringify(map));
        return completed;
    };

    App.getTotalCompletedLessons = function () {
        const map = App.getCompletedTopicsMap();
        let count = 0;
        for (const s in map) {
            for (const lvl in map[s]) {
                count += map[s][lvl].length;
            }
        }
        return count;
    };

    // --- Recently Studied Topics ---
    App.recordRecentTopic = function (subjectId, level, topicId, topicTitle) {
        try {
            const key = getUserKey('recent_topics');
            const data = localStorage.getItem(key);
            let recents = data ? JSON.parse(data) : [];

            // Remove existing duplicate
            recents = recents.filter(item => !(item.subjectId === subjectId && item.topicId === topicId));

            // Insert at front
            recents.unshift({
                subjectId,
                level,
                topicId,
                topicTitle,
                timestamp: new Date().toISOString()
            });

            // Keep top 6
            if (recents.length > 6) recents = recents.slice(0, 6);
            localStorage.setItem(key, JSON.stringify(recents));
        } catch (e) {
            console.error('Failed to record recent topic', e);
        }
    };

    App.getRecentTopics = function () {
        try {
            const data = localStorage.getItem(getUserKey('recent_topics'));
            return data ? JSON.parse(data) : [];
        } catch (e) {
            return [];
        }
    };

    // --- Assignments & Quizzes History ---
    App.getAssignmentHistory = function (subjectId = null, level = null) {
        try {
            const data = localStorage.getItem(getUserKey('assignments'));
            let history = data ? JSON.parse(data) : [];
            if (subjectId) {
                history = history.filter(h => h.subjectId === subjectId);
            }
            if (level) {
                history = history.filter(h => h.level.toLowerCase() === level.toLowerCase());
            }
            return history;
        } catch (e) {
            return [];
        }
    };

    App.recordAssignmentAttempt = function (attempt) {
        try {
            const key = getUserKey('assignments');
            const data = localStorage.getItem(key);
            const history = data ? JSON.parse(data) : [];

            // Add unique attempt id and timestamp
            attempt.id = 'att_' + Date.now();
            attempt.timestamp = new Date().toISOString();

            history.unshift(attempt);
            localStorage.setItem(key, JSON.stringify(history));

            // If passed >= 70%, trigger progression unlock!
            let unlockedLevel = null;
            if (attempt.percentage >= 70) {
                unlockedLevel = App.unlockNextLevel(attempt.subjectId, attempt.level);
            }

            return { success: true, attempt, unlockedLevel };
        } catch (e) {
            console.error('Failed to save assignment attempt:', e);
            return { success: false, error: e };
        }
    };

    // --- UI Toasts ---
    App.showToast = function (message, type = 'info', title = 'EduAdapt-AI') {
        let container = document.getElementById('eduToastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'eduToastContainer';
            container.className = 'toast-container position-fixed top-0 end-0 p-3 edu-toast-container';
            document.body.appendChild(container);
        }

        const icons = {
            success: 'bi-check-circle-fill text-success',
            danger: 'bi-exclamation-triangle-fill text-danger',
            warning: 'bi-exclamation-circle-fill text-warning',
            info: 'bi-info-circle-fill text-primary'
        };

        const toastId = 'toast_' + Date.now();
        const html = `
            <div id="${toastId}" class="toast align-items-center border-0 shadow-lg" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header bg-white">
                    <i class="bi ${icons[type] || icons.info} me-2 fs-5"></i>
                    <strong class="me-auto text-dark">${title}</strong>
                    <small class="text-muted">just now</small>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body bg-white text-dark border-top">
                    ${message}
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
        const toastEl = document.getElementById(toastId);
        if (window.bootstrap && window.bootstrap.Toast) {
            const bsToast = new window.bootstrap.Toast(toastEl, { delay: 4000 });
            bsToast.show();
            toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
        } else {
            setTimeout(() => toastEl.remove(), 4000);
        }
    };

    // --- Code Block Clipboard Hook ---
    App.setupCodeCopy = function () {
        document.querySelectorAll('.code-copy-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const container = btn.closest('.code-container');
                if (!container) return;
                const codeEl = container.querySelector('.code-content');
                if (!codeEl) return;

                navigator.clipboard.writeText(codeEl.innerText).then(() => {
                    const original = btn.innerHTML;
                    btn.innerHTML = '<i class="bi bi-check-lg text-success"></i> Copied!';
                    setTimeout(() => {
                        btn.innerHTML = original;
                    }, 2000);
                }).catch(err => {
                    console.error('Clipboard copy failed:', err);
                });
            });
        });
    };

    // Initialize globally
    window.App = App;

    document.addEventListener('DOMContentLoaded', () => {
        App.setupCodeCopy();

        // Highlight active navbar link
        const currentPath = window.location.pathname.split('/').pop() || 'index.html';
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPath || (currentPath === '' && href === 'index.html')) {
                link.classList.add('active', 'text-primary', 'fw-bold');
            }
        });
    });
})();
