/**
 * EduAdapt-AI - Student Dashboard Controller
 * Computes live statistics, renders selected subjects, unlocks, and recent study milestones.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Guard route
    const user = window.Auth ? window.Auth.requireAuth() : null;
    if (!user) return;

    // 2. Render Student Greeting
    const welcomeNameEl = document.getElementById('dashboardStudentName');
    if (welcomeNameEl) {
        welcomeNameEl.textContent = user.name;
    }

    // 3. Compute & Render Statistics
    renderDashboardStats();

    // 4. Render Selected Subject Cards
    renderEnrolledSubjects();

    // 5. Render Recently Studied Topics
    renderRecentTopics();

    // 6. Render Assignment Summary & Milestones
    renderRecentAssignments();
});

function renderDashboardStats() {
    const selectedSubjects = window.App.getSelectedSubjects();
    const completedLessons = window.App.getTotalCompletedLessons();
    const assignmentHistory = window.App.getAssignmentHistory();

    // Total Subjects
    const statSubjectsEl = document.getElementById('statTotalSubjects');
    if (statSubjectsEl) statSubjectsEl.textContent = selectedSubjects.length;

    // Lessons Completed
    const statLessonsEl = document.getElementById('statCompletedLessons');
    if (statLessonsEl) statLessonsEl.textContent = completedLessons;

    // Assignments Attempted
    const statAssignmentsEl = document.getElementById('statAssignmentsAttempted');
    if (statAssignmentsEl) statAssignmentsEl.textContent = assignmentHistory.length;

    // Average Score
    const statAvgScoreEl = document.getElementById('statAverageScore');
    let avgScore = 0;
    if (assignmentHistory.length > 0) {
        const total = assignmentHistory.reduce((acc, curr) => acc + (curr.percentage || 0), 0);
        avgScore = Math.round(total / assignmentHistory.length);
    }
    if (statAvgScoreEl) statAvgScoreEl.textContent = `${avgScore}%`;

    // Overall Progress Percentage
    // Each enrolled subject has 30 topics total (10 easy, 10 med, 10 comp)
    const statProgressPctEl = document.getElementById('statOverallProgress');
    const statProgressBarEl = document.getElementById('statOverallProgressBar');
    let overallPct = 0;
    const totalPossibleTopics = selectedSubjects.length * 30;
    if (totalPossibleTopics > 0) {
        overallPct = Math.min(100, Math.round((completedLessons / totalPossibleTopics) * 100));
    }
    if (statProgressPctEl) statProgressPctEl.textContent = `${overallPct}%`;
    if (statProgressBarEl) statProgressBarEl.style.width = `${overallPct}%`;
}

function renderEnrolledSubjects() {
    const container = document.getElementById('enrolledSubjectsGrid');
    const emptyState = document.getElementById('noEnrolledSubjectsAlert');
    if (!container) return;

    const selectedIds = window.App.getSelectedSubjects();
    const catalog = window.SUBJECTS_DATA || {};

    if (selectedIds.length === 0) {
        container.innerHTML = '';
        if (emptyState) emptyState.classList.remove('d-none');
        return;
    }

    if (emptyState) emptyState.classList.add('d-none');
    let html = '';

    selectedIds.forEach(subId => {
        const subject = catalog[subId];
        if (!subject) return;

        const levelsState = window.App.getSubjectLevels(subId);
        const completedMap = window.App.getCompletedTopicsMap()[subId] || {};
        
        let completedInSubject = 0;
        ['easy', 'medium', 'complex'].forEach(lvl => {
            if (completedMap[lvl]) completedInSubject += completedMap[lvl].length;
        });

        const subjectProgressPct = Math.round((completedInSubject / 30) * 100);

        // Determine highest unlocked level
        let highestLevel = 'easy';
        let levelBadge = '<span class="badge bg-success-subtle text-success border border-success">Level 1: Easy</span>';
        if (levelsState.completed) {
            highestLevel = 'complex';
            levelBadge = '<span class="badge bg-primary-subtle text-primary border border-primary"><i class="bi bi-patch-check-fill me-1"></i> Mastered</span>';
        } else if (levelsState.complex) {
            highestLevel = 'complex';
            levelBadge = '<span class="badge bg-danger-subtle text-danger border border-danger">Level 3: Complex</span>';
        } else if (levelsState.medium) {
            highestLevel = 'medium';
            levelBadge = '<span class="badge bg-warning-subtle text-warning border border-warning">Level 2: Medium</span>';
        }

        html += `
        <div class="col-md-6 col-xl-6 mb-4">
            <div class="card h-100 shadow-sm border-0 border-top border-4 border-${subject.badge_color || 'primary'}">
                <div class="card-body p-4 d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div class="d-flex align-items-center gap-3">
                            <div class="p-3 rounded-3 bg-light text-${subject.badge_color || 'primary'} fs-3">
                                <i class="bi ${subject.icon || 'bi-book-fill'}"></i>
                            </div>
                            <div>
                                <h5 class="fw-bold mb-1">${subject.title}</h5>
                                <div class="d-flex align-items-center gap-2">
                                    ${levelBadge}
                                    <small class="text-muted">${completedInSubject}/30 Topics</small>
                                </div>
                            </div>
                        </div>
                    </div>

                    <p class="text-secondary small mb-3 flex-grow-1">${subject.short_summary || subject.description}</p>

                    <div class="mb-3">
                        <div class="d-flex justify-content-between small text-muted mb-1">
                            <span>Subject Mastery Progress</span>
                            <span class="fw-bold">${subjectProgressPct}%</span>
                        </div>
                        <div class="progress" style="height: 6px;">
                            <div class="progress-bar bg-${subject.badge_color || 'primary'}" role="progressbar" style="width: ${subjectProgressPct}%"></div>
                        </div>
                    </div>

                    <!-- Level Progression Indicators -->
                    <div class="d-flex gap-1 mb-4">
                        <div class="flex-fill text-center p-1 rounded bg-light border ${levelsState.easy ? 'border-success text-success fw-semibold' : 'text-muted'}" style="font-size: 0.75rem;">
                            <i class="bi ${levelsState.easy ? 'bi-unlock-fill' : 'bi-lock-fill'}"></i> Easy
                        </div>
                        <div class="flex-fill text-center p-1 rounded bg-light border ${levelsState.medium ? 'border-success text-success fw-semibold' : 'text-muted'}" style="font-size: 0.75rem;">
                            <i class="bi ${levelsState.medium ? 'bi-unlock-fill' : 'bi-lock-fill'}"></i> Medium
                        </div>
                        <div class="flex-fill text-center p-1 rounded bg-light border ${levelsState.complex ? 'border-success text-success fw-semibold' : 'text-muted'}" style="font-size: 0.75rem;">
                            <i class="bi ${levelsState.complex ? 'bi-unlock-fill' : 'bi-lock-fill'}"></i> Complex
                        </div>
                    </div>

                    <div class="d-flex gap-2 mt-auto">
                        <a href="study-material.html?subject=${subId}&level=${highestLevel}" class="btn btn-${subject.badge_color || 'primary'} btn-sm flex-grow-1">
                            <i class="bi bi-book-half me-1"></i> Continue Learning
                        </a>
                        <a href="assignments.html?subject=${subId}&level=${highestLevel}" class="btn btn-outline-secondary btn-sm" title="Take Level Assessment">
                            <i class="bi bi-pencil-square me-1"></i> Quiz
                        </a>
                    </div>
                </div>
            </div>
        </div>
        `;
    });

    container.innerHTML = html;
}

function renderRecentTopics() {
    const listEl = document.getElementById('recentTopicsList');
    const emptyEl = document.getElementById('noRecentTopicsAlert');
    if (!listEl) return;

    const recents = window.App.getRecentTopics();
    const catalog = window.SUBJECTS_DATA || {};

    if (!recents || recents.length === 0) {
        listEl.innerHTML = '';
        if (emptyEl) emptyEl.classList.remove('d-none');
        return;
    }

    if (emptyEl) emptyEl.classList.add('d-none');
    let html = '';

    recents.forEach(item => {
        const subject = catalog[item.subjectId];
        const subTitle = subject ? subject.title : item.subjectId;
        const color = subject ? subject.badge_color : 'primary';

        const timeAgo = formatTimeAgo(item.timestamp);

        html += `
        <div class="d-flex align-items-center justify-content-between p-3 bg-white rounded-3 border mb-2 card-hover-lift">
            <div class="d-flex align-items-center gap-3">
                <span class="badge bg-${color}-subtle text-${color} p-2 px-3 text-uppercase" style="font-size: 0.75rem;">${subTitle}</span>
                <div>
                    <h6 class="mb-0 fw-semibold text-truncate" style="max-width: 320px;">${item.topicTitle}</h6>
                    <small class="text-muted"><i class="bi bi-clock me-1"></i>${timeAgo} &bull; <span class="text-capitalize">${item.level}</span> Level</small>
                </div>
            </div>
            <a href="study-material.html?subject=${item.subjectId}&level=${item.level}&topic=${item.topicId}" class="btn btn-outline-primary btn-sm">
                Resume <i class="bi bi-arrow-right ms-1"></i>
            </a>
        </div>
        `;
    });

    listEl.innerHTML = html;
}

function renderRecentAssignments() {
    const tableBody = document.getElementById('recentAssignmentsTableBody');
    const emptyEl = document.getElementById('noAssignmentsAlert');
    if (!tableBody) return;

    const history = window.App.getAssignmentHistory().slice(0, 5); // top 5
    const catalog = window.SUBJECTS_DATA || {};

    if (!history || history.length === 0) {
        tableBody.innerHTML = '';
        if (emptyEl) emptyEl.classList.remove('d-none');
        return;
    }

    if (emptyEl) emptyEl.classList.add('d-none');
    let html = '';

    history.forEach(att => {
        const subject = catalog[att.subjectId];
        const subTitle = subject ? subject.title : att.subjectId;
        const dateStr = new Date(att.timestamp).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
        const passBadge = att.passed 
            ? '<span class="badge bg-success-subtle text-success border border-success"><i class="bi bi-check-circle-fill me-1"></i> Passed</span>'
            : '<span class="badge bg-danger-subtle text-danger border border-danger"><i class="bi bi-x-circle-fill me-1"></i> Failed</span>';

        html += `
        <tr>
            <td class="fw-semibold">${subTitle}</td>
            <td><span class="badge bg-light text-dark text-capitalize border">${att.level}</span></td>
            <td><span class="fw-bold ${att.passed ? 'text-success' : 'text-danger'}">${att.score} / ${att.total} (${att.percentage}%)</span></td>
            <td>${passBadge}</td>
            <td class="text-muted small">${dateStr}</td>
            <td class="text-end">
                <a href="assignments.html?subject=${att.subjectId}&level=${att.level}" class="btn btn-sm btn-outline-secondary">
                    <i class="bi bi-arrow-repeat"></i> Retry
                </a>
            </td>
        </tr>
        `;
    });

    tableBody.innerHTML = html;
}

function formatTimeAgo(isoString) {
    if (!isoString) return 'recently';
    const seconds = Math.floor((new Date() - new Date(isoString)) / 1000);
    if (seconds < 60) return 'just now';
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
}
