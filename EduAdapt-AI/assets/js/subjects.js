/**
 * EduAdapt-AI - Subject Catalog & Enrollment Controller
 * Allows students to enroll in or remove multiple subjects, preview topics, and jump to lessons.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Auth check
    const user = window.Auth ? window.Auth.requireAuth() : null;
    if (!user) return;

    renderSubjectCatalog();
});

function renderSubjectCatalog() {
    const container = document.getElementById('subjectCatalogGrid');
    if (!container) return;

    const catalog = window.SUBJECTS_DATA || {};
    const selectedIds = window.App.getSelectedSubjects();

    let html = '';

    Object.keys(catalog).forEach(subjectId => {
        const subject = catalog[subjectId];
        const isSelected = selectedIds.includes(subjectId);

        // Summarize sample topics from each level
        const easyTopics = (subject.levels.easy.topics || []).slice(0, 3).map(t => t.title.replace(/^\d+\.\s*/, '')).join(', ');
        const medTopics = (subject.levels.medium.topics || []).slice(0, 3).map(t => t.title.replace(/^\d+\.\s*/, '')).join(', ');
        const compTopics = (subject.levels.complex.topics || []).slice(0, 3).map(t => t.title.replace(/^\d+\.\s*/, '')).join(', ');

        const enrolledBadge = isSelected
            ? `<span class="badge bg-success-subtle text-success border border-success"><i class="bi bi-check-circle-fill me-1"></i> Enrolled</span>`
            : `<span class="badge bg-light text-muted border">Available to Enroll</span>`;

        const actionButton = isSelected
            ? `<button class="btn btn-outline-danger btn-sm subject-toggle-btn" data-subject-id="${subjectId}" data-action="remove">
                 <i class="bi bi-dash-circle me-1"></i> Remove from My Courses
               </button>`
            : `<button class="btn btn-primary btn-sm subject-toggle-btn" data-subject-id="${subjectId}" data-action="add">
                 <i class="bi bi-plus-circle me-1"></i> Select & Enroll
               </button>`;

        const continueBtn = isSelected
            ? `<a href="study-material.html?subject=${subjectId}&level=easy" class="btn btn-outline-primary btn-sm">
                 <i class="bi bi-arrow-right-circle me-1"></i> Continue Learning
               </a>`
            : `<button class="btn btn-outline-secondary btn-sm" disabled title="Enroll to start studying">
                 <i class="bi bi-lock me-1"></i> Locked
               </button>`;

        html += `
        <div class="col-lg-6 mb-4">
            <div class="card h-100 shadow-sm border-0 border-top border-4 border-${subject.badge_color || 'primary'}">
                <div class="card-body p-4 d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div class="d-flex align-items-center gap-3">
                            <div class="p-3 rounded-3 bg-light text-${subject.badge_color || 'primary'} fs-3">
                                <i class="bi ${subject.icon || 'bi-book-fill'}"></i>
                            </div>
                            <div>
                                <h4 class="fw-bold mb-1">${subject.title}</h4>
                                <div class="d-flex align-items-center gap-2">
                                    ${enrolledBadge}
                                    <span class="badge bg-info-subtle text-info border border-info">${subject.difficulty || 'All Levels'}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <p class="text-secondary mb-3">${subject.description}</p>

                    <!-- Topics Count & Overview -->
                    <div class="bg-light p-3 rounded-3 mb-3 border">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="fw-bold small text-dark"><i class="bi bi-layers-fill text-primary me-1"></i> Curriculum Scope</span>
                            <span class="badge bg-primary">30 Comprehensive Topics</span>
                        </div>
                        <ul class="list-unstyled mb-0 small text-muted">
                            <li class="mb-1"><strong>🟢 Easy (10 Topics):</strong> ${easyTopics}...</li>
                            <li class="mb-1"><strong>🟡 Medium (10 Topics):</strong> ${medTopics}...</li>
                            <li><strong>🔴 Complex (10 Topics):</strong> ${compTopics}...</li>
                        </ul>
                    </div>

                    <div class="d-flex align-items-center justify-content-between mt-auto pt-2 border-top">
                        <div class="d-flex gap-2">
                            ${actionButton}
                        </div>
                        <div>
                            ${continueBtn}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;
    });

    container.innerHTML = html;

    // Attach click listeners to toggle buttons
    container.querySelectorAll('.subject-toggle-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const subjectId = btn.getAttribute('data-subject-id');
            const action = btn.getAttribute('data-action');
            const subject = catalog[subjectId];

            if (action === 'add') {
                window.App.addSubject(subjectId);
                window.App.showToast(`Enrolled in <strong>${subject.title}</strong>! Added to your dashboard.`, 'success');
            } else {
                window.App.removeSubject(subjectId);
                window.App.showToast(`Removed <strong>${subject.title}</strong> from your selected courses.`, 'warning');
            }

            // Re-render
            renderSubjectCatalog();
        });
    });
}
