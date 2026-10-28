# EduAdapt-AI — Personalized Student Learning Platform

> **Frontend-Only Educational Web Application**  
> Built with HTML5, CSS3, Vanilla JavaScript, Bootstrap 5, and Browser `localStorage`.

---

## 🌟 Overview

**EduAdapt-AI** is a modern, responsive, and fully functional personalized educational web application designed to guide computer science students through structured, adaptive learning paths. 

The platform supports four core disciplines:
1. **Python Programming**
2. **Java Programming**
3. **Database Management Systems (DBMS) & SQL**
4. **Data Structures and Algorithms (DSA)**

Each subject features a three-tier progression model (**Easy**, **Medium**, and **Complex**) containing **10 comprehensive, richly documented topics per level (120 lessons total)**, paired with **120 multiple-choice assessment questions (10 questions per assessment)**, and a **24/7 offline rule-based AI Tutor**.

---

## ⚡ Important Technical Restrictions & Architecture

This application is strictly **100% Frontend-Only**:
- **Technology Stack**: HTML5, CSS3, Vanilla JavaScript (ES6+), Bootstrap 5.3.3 (via CDN), and Bootstrap Icons.
- **Data Persistence**: Browser `localStorage` and `sessionStorage`.
- **Zero Backend Dependencies**:
  - ❌ NO Python, Flask, FastAPI, or Django
  - ❌ NO Node.js, Express, or npm build steps
  - ❌ NO Java, Spring Boot, or PHP
  - ❌ NO MySQL, SQLite, PostgreSQL, or database daemons
  - ❌ NO Docker, Kubernetes, Azure, or FFmpeg
  - ❌ NO Paid third-party APIs or cloud subscriptions

The entire application runs directly as a static website. You can open `index.html` directly in any modern web browser or host it for free on **GitHub Pages**, **Netlify**, or **Vercel**.

---

## ⚠️ Academic & Demonstration Disclaimers

> [!IMPORTANT]
> **Client-Side Authentication Disclaimer**  
> Authentication in EduAdapt-AI operates entirely within the client's browser using `localStorage`. This architecture is designed specifically for standalone evaluation, frontend portfolio demonstrations, and static hosting without server costs.  
> In real-world enterprise environments, secure authentication strictly requires server-side validation, password hashing (e.g. Argon2, BCrypt), secure HTTP-only cookies or signed JWTs, and database storage.

> [!NOTE]
> **Assessment Scoring & Answer Keys**  
> Assessment grading, answer verification, and level unlock flags are computed on the client side in JavaScript. Because there is no backend server verifying answers, these client-side scores can be inspected or modified via browser Developer Tools and should not be used as tamper-proof examinations.

---

## 🚀 Key Features

### 1. Modern Login & Registration
- **Student Registration**: Register with Full Name, Email, and Password with real-time form validation.
- **Student Login**: Authenticate using registered credentials.
- **One-Click Demo User**: Instant autofill button for demo student **Alex Morgan** (`alex@eduadapt.io` / `password123`).
- **Password Visibility Toggle**: Interactive show/hide toggle for password fields.
- **Route Protection**: JavaScript session checks (`Auth.requireAuth()`) guard application pages, redirecting unauthenticated visitors to `index.html`.
- **Student Personalization**: Student's name and email dynamically appear in navigation bars, greetings, and avatar dropdowns.

### 2. Personalized Student Dashboard
- **Live Statistics**:
  - Total Enrolled Subjects count
  - Completed Lessons count
  - Assessments Attempted count
  - Average Assessment Score percentage
  - Overall Course Progress percentage bar
- **Enrolled Subject Cards**:
  - Subject title, icon, and description
  - Current difficulty badge (Level 1: Easy, Level 2: Medium, Level 3: Complex, or Mastered)
  - Topic completion counter (e.g. `12 / 30 Topics`) and progress bar
  - Direct "Continue Learning" and "Take Quiz" action links
- **Recently Studied Lessons**: Dynamic list of the student's recent topics with timestamp ("5m ago", "2h ago") and one-click "Resume" buttons.
- **Assessment History**: Table of recent quiz attempts with scores, pass/fail status, and retake buttons.
- **Empty States**: Clear and encouraging empty states when no courses are enrolled or no quizzes have been attempted yet.

### 3. Subject Catalog & Multiple Enrollment
- **4 Computer Science Subjects**:
  - Python Programming
  - Java Programming
  - Database Management Systems (DBMS)
  - Data Structures and Algorithms
- **Curriculum Scope**: Displays topic count (30 topics across 3 levels) and previews of topics covered in each level.
- **Enrollment Toggle**: Students can enroll in or remove multiple subjects. Selections persist in `localStorage`, and duplicate enrollments are automatically prevented.

### 4. Comprehensive Study Material (120 Lessons)
- **100% In-Page Content**: All content is presented directly in web pages—no external PDFs or downloads required.
- **120 High-Quality Topics**: Exactly 10 meaningful, detailed topics per level across 4 subjects (10 Easy + 10 Medium + 10 Complex $\times$ 4 Subjects = 120 topics). No placeholder filler text.
- **Structured Topic View**:
  - Topic Title & reading time badge
  - Learning Objectives milestone card
  - In-depth theoretical explanation with definitions
  - Formal Syntax block with one-click copy button
  - Working code example with one-click copy button
  - Expected terminal/console execution output
  - Common Pitfalls & Debugging Callout
  - Interactive Practice Question with "Reveal Solution" toggle
  - Previous and Next Topic navigation buttons
  - "Mark as Completed" button that updates sidebar checkmarks and dashboard progress
- **Topic Search Field**: Live real-time filter to quickly find lessons in the curriculum sidebar.

### 5. Graded Assessments & Level Progression
- **12 Assessments (120 Multiple Choice Questions)**:
  - 10 questions per level per subject.
  - 4 answer options (A, B, C, D) per question with single correct answer.
  - Thorough pedagogical explanations for every question.
- **Quiz Engine**:
  - One question at a time with counter and progress bar.
  - Jump-to-question navigation pills showing answered vs unanswered questions.
  - Submit confirmation preventing accidental premature submissions.
- **Level Progression Rules**:
  - **Easy (Level 1)**: Unlocked by default upon enrollment.
  - **Medium (Level 2)**: Automatically unlocks when scoring **70% or higher** on Easy assessment.
  - **Complex (Level 3)**: Automatically unlocks when scoring **70% or higher** on Medium assessment.
  - **Subject Mastery**: Scoring $\ge 70\%$ on Complex assessment awards the Subject Mastery badge.
  - **JavaScript Access Verification**: Before rendering any level or quiz, JavaScript verifies that the prerequisite level is passed. Manually changing URL parameters (e.g. `?level=complex`) displays a locked level banner with a link to complete the prerequisite quiz.
- **Results Review Page (`results.html`)**:
  - Score percentage and pass/fail banner.
  - Newly unlocked tier notification alert.
  - Full question-by-question review showing the student's answer, correct answer, and pedagogical explanation.
  - Retry Assessment button allowing unlimited retakes.

### 6. Rule-Based AI Tutor Chatbot
- **Accessible Everywhere**: Floating chat dock button available on every page, plus a dedicated full-page experience at `chatbot.html`.
- **Zero Backend / Zero Cloud Cost**: Completely self-contained JavaScript rule-based engine.
- **Educational Capabilities**:
  - In-depth concept reviews for Python (decorators, generators, comprehensions, OOP).
  - Java architecture (JVM memory, StringBuilder immutability, Streams, multithreading).
  - DBMS theory (1NF to BCNF normalization, ACID properties, SQL joins, B+ Trees).
  - DSA analysis (Big-O asymptotic bounds, Binary Search, Trees, Dynamic Programming).
  - Debugging common errors (`IndexError`, `NullPointerException`, `AttributeError`).
  - Assignment hints and clues without spoiling direct answers.
  - Interactive "Quiz me on [subject]" mini-challenges.
  - Context-aware answers based on the student's current active lesson.
  - Honest fallback when questions exceed local scope, with suggested relevant prompts.
  - Chat history persistence in `localStorage` with a "Clear Conversation" option.

---

## 📁 Project Structure

```
cnad_project/
├── index.html               # Landing page & student login interface
├── register.html            # Student registration page
├── dashboard.html           # Personalized student dashboard & statistics
├── subjects.html            # Subject selection catalog & enrollment
├── study-material.html      # 120-topic curriculum reader & search
├── assignments.html         # 10-question MCQ quiz player & history
├── results.html             # Detailed assessment review & explanations
├── chatbot.html             # Dedicated AI Tutor chat page
├── README.md                # Comprehensive documentation & deployment guide
├── .gitignore               # Git ignore rules for static projects
│
├── assets/
│   ├── css/
│   │   └── style.css        # Custom styling, dark code blocks & responsive UI
│   │
│   ├── js/
│   │   ├── study-content.js # Complete curriculum data (120 topics)
│   │   ├── assignment-data.js# Complete assessment questions (120 MCQs)
│   │   ├── auth.js          # Client-side demo authentication & route guards
│   │   ├── app.js           # Core state manager, progress tracking & toast alerts
│   │   ├── dashboard.js     # Live statistics computation & enrolled subject cards
│   │   ├── subjects.js      # Subject enrollment catalog controller
│   │   ├── learning.js      # Curriculum reader, level gatekeeper & topic search
│   │   ├── assignments.js   # Quiz player engine, grading & results review
│   │   └── chatbot.js       # Offline rule-based educational AI tutor
│   │
│   └── images/              # Image assets directory
│
└── EduAdapt-AI/             # Standalone mirror copy of all frontend files
    ├── index.html
    ├── register.html
    ├── dashboard.html
    ├── subjects.html
    ├── study-material.html
    ├── assignments.html
    ├── results.html
    ├── chatbot.html
    └── assets/...
```

---

## 💻 Local Testing Instructions

Because EduAdapt-AI is frontend-only, you can test it locally in seconds without installing compilers, runtimes, or database servers.

### Method 1: Direct File Opening (Simplest)
1. Navigate to the project directory in your file manager (Windows File Explorer, macOS Finder, or Linux Files).
2. Double-click `index.html`.
3. The application will open directly in your default browser (`file:///.../index.html`).

### Method 2: Python Static Preview Server (Recommended)
If Python is installed on your computer, launch a local web server:
```bash
# From the project root directory
python -m http.server 8000
```
Open your browser and navigate to:
```
http://localhost:8000
```

### Method 3: VS Code Live Server
1. Open the project folder in **Visual Studio Code**.
2. Install the **Live Server** extension by Ritwick Dey.
3. Right-click on `index.html` and click **"Open with Live Server"**.

### Method 4: Node `npx serve`
If Node.js is installed on your computer:
```bash
npx serve .
```

---

## 🚀 Static Website Deployment Guide

EduAdapt-AI requires **zero build steps** and uses clean relative paths (`assets/...`). It can be deployed directly to any static web host.

### Option 1: GitHub Pages (Free & Recommended)

1. **Create a GitHub Repository**:
   - Go to [GitHub](https://github.com) and create a new public repository (e.g., `eduadapt-ai`).
2. **Initialize and Push Frontend Files**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: EduAdapt-AI Frontend Platform"
   git branch -M main
   git remote add origin https://github.com/<your-username>/eduadapt-ai.git
   git push -u origin main
   ```
3. **Enable GitHub Pages**:
   - Open your repository on GitHub.
   - Click **Settings** (tab at top).
   - In the left sidebar, click **Pages**.
   - Under **Build and deployment > Source**, select **Deploy from a branch**.
   - Under **Branch**, select `main` and folder `/ (root)`.
   - Click **Save**.
4. **Access Your Live Site**:
   - After 1–2 minutes, your live site URL will appear at:
     ```
     https://<your-username>.github.io/eduadapt-ai/
     ```

---

### Option 2: Netlify (Drag-and-Drop or Git)

#### Drag-and-Drop (Zero Terminal):
1. Go to [Netlify](https://app.netlify.com) and log in.
2. Go to the **Sites** tab.
3. Drag and drop the `cnad_project` folder (or `EduAdapt-AI` folder) into the **"Drag and drop your site output folder here"** area.
4. Netlify will deploy the site instantly and give you a public URL (e.g. `https://eduadapt-ai-demo.netlify.app`).

#### Via Git:
1. Click **Add new site > Import an existing project**.
2. Connect your GitHub repository.
3. Leave **Build command** empty.
4. Set **Publish directory** to `.` (or `EduAdapt-AI`).
5. Click **Deploy Site**.

---

### Option 3: Vercel Static Hosting

1. Install the Vercel CLI (or connect via GitHub on [vercel.com](https://vercel.com)):
   ```bash
   npm i -g vercel
   ```
2. Run deployment from the root directory:
   ```bash
   vercel --prod
   ```
3. Select defaults (Framework: `Other`, Build command: None, Output directory: `.`).
4. Vercel provides an instant global CDN URL.

---

## 🧪 Functional Verification & Testing Walkthrough

Follow this step-by-step checklist to test all features:

| Feature | Step | Expected Result |
| :--- | :--- | :--- |
| **1. Registration** | Open `register.html`, fill in Name, Email, Password, and submit. | Account is created in `localStorage`, user is auto-logged in, and redirected to `dashboard.html`. |
| **2. Demo Login** | Open `index.html`, click *"Autofill Demo Student"*, then *"Sign In"*. | Form fills with `alex@eduadapt.io` / `password123` and logs in instantly. |
| **3. Password Toggle** | Click the eye icon next to the password input. | Password toggles between masked (`password`) and plaintext (`text`). |
| **4. Dashboard Greeting** | View the dashboard header. | Student's name ("Alex Morgan") is displayed with greeting. |
| **5. Subject Selection** | Go to `subjects.html`, click *"Remove from My Courses"* on Python, then *"Select & Enroll"*. | Toast alert confirms update; only enrolled courses appear on `dashboard.html`. |
| **6. Curriculum Navigation** | Open `study-material.html`, switch between Python, Java, DBMS, and DSA. | Topics list updates instantly to 10 topics for that subject. |
| **7. Topic Search** | Type *"loop"* or *"join"* into the sidebar search box. | Topics filter in real time; unmatched topics are hidden. |
| **8. Code Copying** | Click the *"Copy"* button on any code block. | Button changes to *"Copied!"* and code is copied to clipboard. |
| **9. Practice Questions** | In any topic, click *"Reveal Solution"*. | Correct answer card smoothly appears/toggles. |
| **10. Lesson Completion** | Click *"Mark as Completed"* on a topic. | Button turns green, checkmark appears on sidebar, and dashboard progress increments. |
| **11. Quiz Execution** | Go to `assignments.html`, answer all 10 questions, and submit. | Answers are recorded; user is redirected to `results.html` with percentage score. |
| **12. Level Progression** | Score $\ge 70\%$ on an Easy assessment. | Results page shows *"Level MEDIUM is now unlocked!"*; Medium becomes clickable in curriculum and quizzes. |
| **13. Access Gate Check** | Manually type `study-material.html?subject=dsa&level=complex` before passing Medium. | JavaScript checks access, prevents rendering, and shows *"Level Locked"* banner with prerequisite quiz link. |
| **14. AI Tutor Chatbot** | Click the floating chat button on any page or go to `chatbot.html`. | Type *"Explain Big-O"* or click *"Quiz me on Python"*. Tutor replies accurately with formatting and code blocks. |
| **15. Persistence Test** | Refresh the browser or close and reopen the tab. | Enrolled courses, completed lessons, unlocked levels, and quiz scores remain preserved in `localStorage`. |

---

## 🔧 Troubleshooting & Frequently Asked Questions

### 1. The page looks unstyled or fonts/icons fail to load
- Ensure your computer has an active internet connection so Bootstrap 5 CSS and Bootstrap Icons load from the CDN (`cdn.jsdelivr.net`).
- If testing in an offline environment, all scripts still function because the core logic is self-contained.

### 2. Relative paths are broken or 404s appear
- All links use relative paths (`index.html`, `dashboard.html`, `assets/css/style.css`, `assets/js/...`).
- Ensure the folder structure is kept intact when uploading to GitHub or static hosting.

### 3. How do I reset all demo data and start fresh?
- Open your browser's Developer Tools (press `F12` or `Ctrl+Shift+I`).
- Go to the **Application** (or **Storage**) tab.
- Click **Local Storage** in the left sidebar, right-click your domain/file origin, and click **Clear**.
- Refresh the page. EduAdapt-AI will re-seed the default Alex Morgan demo account.

---

## 📄 License & Attribution

Designed and developed for **EduAdapt-AI — Personalized Student Learning Platform**.  
Pure static frontend architecture adhering to strict technical guidelines.
