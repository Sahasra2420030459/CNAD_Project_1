# VideoCloud Frontend - Web Dashboard

React Single-Page Application (SPA) for **The Cloud-Based Asynchronous Video Compression and Batch Processing Platform**.

---

## 🚀 Features

- **Sidebar Navigation**: Instant switching between Dashboard, Upload Videos, Processing Jobs, History & Analytics, and System Settings.
- **Summary Metrics**: Real-time cards for Total Ingested Videos, Queued, Processing (FFmpeg active), Completed, and Failed.
- **Drag-and-Drop Ingestion**: Multi-file drag-and-drop zone with instant client-side validation for file types (`.mp4`, `.mov`, `.mkv`, `.avi`, `.webm`) and maximum 500MB size limit.
- **Staged Video Previews**: Review staged video name, size, container format, and estimated compression savings prior to batch submission, with single-click removal.
- **Preset Customization**: Three fine-tuned FFmpeg transcoding presets:
  - `LOW`: 1080p (Full HD), CRF 22, audio 192k (High Fidelity)
  - `MEDIUM`: 720p (HD), CRF 28, audio 128k (Balanced Web Default)
  - `HIGH`: 480p (SD), CRF 32, audio 96k (Max Storage Savings)
- **Target Containers**: Choose between universal MP4, WebM, or MKV containers.
- **Live Status Progression**: Real-time visual tracking of `QUEUED`, `PROCESSING`, `COMPLETED`, and `FAILED` states with progress bars and auto-polling (which stops automatically when no jobs are active).
- **Secure File Downloads**: Trigger streaming downloads directly from the authenticated backend with browser blob handlers.
- **One-Click Retry**: Re-enqueue failed jobs with a single click.
- **Strict Security Compliance**: JWT tokens are maintained exclusively in memory / tab-session scope. `localStorage` persistence is strictly disabled.
- **Accessible & Responsive**: Keyboard navigable with ARIA landmarks, high contrast focus rings, and responsive drawer on mobile screens.

---

## 📦 Prerequisites

- **Node.js**: Version 18.x or 20.x LTS ([Download Node.js](https://nodejs.org/))
- **npm**: Version 9.x or 10.x (bundled with Node.js)

---

## ⚡ Installation & Execution Commands

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Backend API Endpoint (Optional)
The frontend connects to `http://localhost:8080/api` by default. To point to an Azure App Service or custom host, create a `.env` file:
```env
REACT_APP_API_BASE_URL=http://localhost:8080/api
```

### 3. Start Development Server
```bash
npm start
```
The browser will automatically open at `http://localhost:3000`.

### 4. Build for Production (Azure Static Web Apps)
```bash
npm run build
```
Creates an optimized production bundle in the `build/` directory ready for deployment to **Azure Static Web Apps** or an Nginx web server.

---

## 🐳 Docker Execution

To build and run the frontend inside a container without installing Node.js locally:
```bash
# Build standalone container
docker build -t videoplatform-frontend ./frontend

# Run container on port 3000
docker run -p 3000:80 videoplatform-frontend
```
Or start the complete multi-tier stack from the project root:
```bash
docker compose up --build frontend
```
