# The Cloud-Based Asynchronous Video Compression and Batch Processing Platform

An enterprise-ready, cloud-native asynchronous video processing platform built with **Java Spring Boot**, **React.js**, **Docker**, **FFmpeg**, and **Microsoft Azure**.

---

## 🚀 Key Features

- **Batch & Single Ingestion**: Drag-and-drop single or multiple high-definition videos with client and server-side MIME type and size validation.
- **Asynchronous Decoupling**: Offloads compute-heavy transcoding from the REST API to dedicated worker nodes using message queues.
- **FFmpeg Transcoding Engine**: Configurable compression presets (`LOW`, `MEDIUM`, `HIGH`) tuning CRF (Constant Rate Factor), resolution downscaling (1080p, 720p, 480p), and audio bitrate.
- **Job Lifecycle Tracking**: Real-time status progression (`QUEUED` ➔ `PROCESSING` ➔ `COMPLETED` / `FAILED`).
- **Comprehensive Analytics**: Displays original size, compressed size, storage savings percentage, transcode duration, and worker logs.
- **Zero-Cloud Local Mode**: Runs 100% locally with local disk storage adapter and in-memory queue, requiring no Azure accounts or credentials.
- **Seamless Cloud Transition**: Switch from local storage to Azure Blob Storage and Azure Queue Storage via a single environment variable change (`STORAGE_TYPE=azure`, `QUEUE_TYPE=azure`).
- **Enterprise Security**: Spring Security with stateless JWT authentication, password hashing with BCrypt, and strict tenant-isolated video downloads.

---

## 🛠 Technology Stack

| Domain | Technology / Service |
| :--- | :--- |
| **Frontend** | React 18, JavaScript ES6+, HTML5 Drag & Drop, CSS3 Flex/Grid, Axios |
| **Backend API** | Java 21, Spring Boot 3.3.5, Spring Security, Spring Data JPA / Hibernate |
| **Transcoding Worker** | Java 21 Background Worker, FFmpeg CLI, Multi-threading |
| **Database** | MySQL 8.0 / Azure Database for MySQL Flexible Server |
| **Cloud Storage** | Azure Blob Storage (with Local Disk Storage fallback adapter) |
| **Messaging Queue** | Azure Queue Storage (with Local Queue fallback adapter) |
| **Containerization** | Docker, Docker Compose, Multi-stage Dockerfiles |
| **Cloud Hosting** | Azure App Service (Backend), Azure Container Apps (Worker), Azure Static Web Apps (Frontend) |

---

## 📁 Repository Structure

```
cnad_project/
├── backend/                  # Spring Boot REST API, Security, Storage & Queue Abstractions
├── worker/                   # Background Java Transcoding Worker with FFmpeg Engine
├── frontend/                 # React.js Single Page Application UI
├── docs/                     # Architecture, API Spec, Local Dev, and Azure Cloud Guides
│   ├── ARCHITECTURE.md
│   ├── API_SPECIFICATION.md
│   ├── LOCAL_DEVELOPMENT.md
│   └── AZURE_DEPLOYMENT.md
├── docker-compose.yml        # Multi-container orchestration (MySQL, Backend, Worker, Frontend)
├── .env.example              # Central configuration template
└── README.md
```

---

## ⚡ Quick Start (Local Development)

### Option 1: One-Click Docker Compose
Ensure Docker Desktop is running, then:
```powershell
# 1. Clone & copy environment configuration
cp .env.example .env

# 2. Spin up the entire stack
docker compose up --build -d

# 3. Access applications:
#    Frontend: http://localhost:3000
#    Backend API: http://localhost:8080/api
#    Health: http://localhost:8080/api/health
```

### Option 2: Running Without Docker
See [docs/LOCAL_DEVELOPMENT.md](file:///c:/Users/Sahas_sp30gy0/OneDrive/Desktop/cnad_project/docs/LOCAL_DEVELOPMENT.md) for step-by-step instructions to run MySQL, Backend, Worker, and React UI natively on your machine.

---

## ☁️ Azure Cloud Deployment

To deploy to Azure App Service, Azure Container Apps, Azure Blob & Queue Storage, and Azure Database for MySQL, follow the detailed production instructions in [docs/AZURE_DEPLOYMENT.md](file:///c:/Users/Sahas_sp30gy0/OneDrive/Desktop/cnad_project/docs/AZURE_DEPLOYMENT.md).

---

## 🧪 Testing

Run backend logic and storage tests:
```powershell
cd backend
mvn test
```

Run worker transcoding tests:
```powershell
cd worker
mvn test
```
