/**
 * EduAdapt-AI - Client-Side Demo Authentication Module
 * Manages user registration, login, logout, and protected route gating via browser localStorage.
 * 
 * NOTE: This is a frontend demonstration. In production environments, secure authentication
 * requires server-side validation, password hashing (e.g. bcrypt/argon2), and HTTP-only session cookies or JWTs.
 */

(function () {
    const STORAGE_KEY_USER = 'eduadapt_user';
    const STORAGE_KEY_USERS = 'eduadapt_registered_users';

    // Seed default demo user if not already present
    function initDefaultUser() {
        const users = getUsers();
        if (!users || users.length === 0) {
            const defaultDemo = {
                id: 'usr_demo_alex',
                name: 'Alex Morgan',
                email: 'alex@eduadapt.io',
                password: 'password123',
                createdAt: new Date().toISOString()
            };
            saveUsers([defaultDemo]);
        }
    }

    function getUsers() {
        try {
            const data = localStorage.getItem(STORAGE_KEY_USERS);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            console.error('Failed to parse registered users from localStorage', e);
            return [];
        }
    }

    function saveUsers(users) {
        localStorage.setItem(STORAGE_KEY_USERS, JSON.stringify(users));
    }

    function getCurrentUser() {
        try {
            const data = localStorage.getItem(STORAGE_KEY_USER);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.error('Failed to parse current user from localStorage', e);
            return null;
        }
    }

    function setCurrentUser(user) {
        // Strip sensitive fields before setting active session
        const sessionUser = {
            id: user.id || 'usr_' + Date.now(),
            name: user.name,
            email: user.email,
            loggedInAt: new Date().toISOString()
        };
        localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(sessionUser));
    }

    function register(name, email, password) {
        name = name.trim();
        email = email.trim().toLowerCase();
        password = password.trim();

        if (!name || name.length < 2) {
            return { success: false, message: 'Please enter a valid full name (at least 2 characters).' };
        }
        if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            return { success: false, message: 'Please provide a valid email address.' };
        }
        if (!password || password.length < 6) {
            return { success: false, message: 'Password must be at least 6 characters in length.' };
        }

        const users = getUsers();
        const existing = users.find(u => u.email.toLowerCase() === email);
        if (existing) {
            return { success: false, message: 'An account with this email address already exists. Please log in.' };
        }

        const newUser = {
            id: 'usr_' + Date.now(),
            name: name,
            email: email,
            password: password,
            createdAt: new Date().toISOString()
        };
        users.push(newUser);
        saveUsers(users);

        // Auto-login newly registered user
        setCurrentUser(newUser);

        // Initialize default subject enrollments for new student (Python + DBMS by default)
        const userSubjKey = `eduadapt_selected_subjects_${newUser.email}`;
        if (!localStorage.getItem(userSubjKey)) {
            localStorage.setItem(userSubjKey, JSON.stringify(['python', 'dbms']));
        }

        // Initialize level unlock progression
        const userLevelsKey = `eduadapt_levels_${newUser.email}`;
        if (!localStorage.getItem(userLevelsKey)) {
            localStorage.setItem(userLevelsKey, JSON.stringify({
                python: { easy: true, medium: false, complex: false, completed: false },
                java: { easy: true, medium: false, complex: false, completed: false },
                dbms: { easy: true, medium: false, complex: false, completed: false },
                dsa: { easy: true, medium: false, complex: false, completed: false }
            }));
        }

        return { success: true, user: newUser };
    }

    function login(email, password) {
        email = email.trim().toLowerCase();
        password = password.trim();

        if (!email || !password) {
            return { success: false, message: 'Please enter both your email and password.' };
        }

        const users = getUsers();
        const found = users.find(u => u.email.toLowerCase() === email);

        if (!found) {
            return { success: false, message: 'No registered student found with this email. Please register first.' };
        }
        if (found.password !== password) {
            return { success: false, message: 'Incorrect password. Please verify and try again.' };
        }

        setCurrentUser(found);

        // Ensure default enrollments exist
        const userSubjKey = `eduadapt_selected_subjects_${found.email}`;
        if (!localStorage.getItem(userSubjKey)) {
            localStorage.setItem(userSubjKey, JSON.stringify(['python', 'dbms']));
        }
        const userLevelsKey = `eduadapt_levels_${found.email}`;
        if (!localStorage.getItem(userLevelsKey)) {
            localStorage.setItem(userLevelsKey, JSON.stringify({
                python: { easy: true, medium: false, complex: false, completed: false },
                java: { easy: true, medium: false, complex: false, completed: false },
                dbms: { easy: true, medium: false, complex: false, completed: false },
                dsa: { easy: true, medium: false, complex: false, completed: false }
            }));
        }

        return { success: true, user: found };
    }

    function logout() {
        localStorage.removeItem(STORAGE_KEY_USER);
        window.location.href = 'index.html';
    }

    function requireAuth() {
        const user = getCurrentUser();
        if (!user) {
            // Not logged in -> redirect to login/index
            window.location.href = 'index.html?auth_required=1';
            return null;
        }
        return user;
    }

    function redirectIfAuth() {
        const user = getCurrentUser();
        if (user) {
            window.location.href = 'dashboard.html';
        }
    }

    function updateNavUserInfo() {
        const user = getCurrentUser();
        const guestElements = document.querySelectorAll('.auth-guest-only');
        const userElements = document.querySelectorAll('.auth-user-only');
        const nameSpans = document.querySelectorAll('.current-user-name');
        const emailSpans = document.querySelectorAll('.current-user-email');

        if (user) {
            guestElements.forEach(el => el.classList.add('d-none'));
            userElements.forEach(el => el.classList.remove('d-none'));
            nameSpans.forEach(el => el.textContent = user.name);
            emailSpans.forEach(el => el.textContent = user.email);
        } else {
            guestElements.forEach(el => el.classList.remove('d-none'));
            userElements.forEach(el => el.classList.add('d-none'));
        }
    }

    function setupPasswordToggles() {
        document.querySelectorAll('.password-toggle-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const targetId = btn.getAttribute('data-target');
                const input = document.getElementById(targetId);
                const icon = btn.querySelector('i');
                if (!input) return;

                if (input.type === 'password') {
                    input.type = 'text';
                    if (icon) {
                        icon.classList.remove('bi-eye');
                        icon.classList.add('bi-eye-slash');
                    }
                } else {
                    input.type = 'password';
                    if (icon) {
                        icon.classList.remove('bi-eye-slash');
                        icon.classList.add('bi-eye');
                    }
                }
            });
        });
    }

    // Initialize on page load
    document.addEventListener('DOMContentLoaded', () => {
        initDefaultUser();
        updateNavUserInfo();
        setupPasswordToggles();

        // Bind global logout buttons
        document.querySelectorAll('.btn-logout-trigger').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                logout();
            });
        });
    });

    // Public API
    window.Auth = {
        getCurrentUser,
        setCurrentUser,
        getUsers,
        register,
        login,
        logout,
        requireAuth,
        redirectIfAuth,
        updateNavUserInfo
    };
})();
