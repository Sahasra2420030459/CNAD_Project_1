# Local Development Guide

This platform is engineered to run 100% locally on your development machine without any Azure subscription, cloud charges, or external internet access.

---

## 1. Prerequisites

- **Java JDK**: Version 17 or 21 (JDK 21 installed at `C:\Program Files\Java\jdk-21\bin\java.exe`).
- **Node.js & npm**: Node.js 18+ or 20+ for the React frontend.
- **MySQL**: Local MySQL 8.0 server OR Docker with Docker Compose.
- **FFmpeg** (Optional for local testing): If not installed in PATH, the worker's smart fallback simulation mode automatically handles test transcoding.

---

## 2. Fast Start with Docker Compose

If you have Docker Desktop running, you can launch the complete end-to-end stack with a single command:

```powershell
# Copy environment configuration
cp .env.example .env

# Build and start all 4 containers (MySQL, Backend, Worker, Frontend)
docker compose up --build -d

# Check running status
docker compose ps

# View backend logs
docker compose logs -f backend

# View worker compression logs
docker compose logs -f worker
```

Services will be accessible at:
- **Frontend Web UI**: http://localhost:3000
- **Backend REST API**: http://localhost:8080/api
- **Swagger / Health Check**: http://localhost:8080/api/health
- **MySQL Database**: `localhost:3306` (database: `videoplatform`, user: `videouser`, pass: `rootpassword`)

---

## 3. Running Services Locally Without Docker

### 3.1 Start Local MySQL Database
Ensure your local MySQL service is running and create the database:
```sql
CREATE DATABASE IF NOT EXISTS videoplatform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
Or execute the schema script located at `backend/src/main/resources/db/schema.sql`.

### 3.2 Run the Spring Boot Backend API
Navigate to the `backend` directory:
```powershell
cd backend

# Run with Maven Wrapper or Maven
mvn spring-boot:run -Dspring-boot.run.profiles=local
```
Or with Gradle:
```powershell
./gradlew bootRun --args='--spring.profiles.active=local'
```

Key environment properties active in local mode:
- `STORAGE_TYPE=local` (videos saved under `./uploads/originals` and `./uploads/compressed`)
- `QUEUE_TYPE=local` (uses in-memory thread queue / DB queue)
- `SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/videoplatform?useSSL=false`

### 3.3 Run the Background Video Worker
In a separate terminal window:
```powershell
cd worker

mvn spring-boot:run -Dspring-boot.run.profiles=local
```
The worker will:
1. Poll the queue every 3 seconds (`WORKER_POLL_INTERVAL_MS=3000`).
2. Detect pending jobs with status `QUEUED`.
3. Pick up the original video, apply FFmpeg compression (or simulated transcoding if FFmpeg is absent).
4. Save the compressed video to `./uploads/compressed/`.
5. Update the job status to `COMPLETED` and calculate saved storage metrics.

### 3.4 Run the React Frontend
In a separate terminal window:
```powershell
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```
The browser opens automatically at `http://localhost:3000`.

---

## 4. Default Test Credentials

For quick evaluation, you can register a new account on the UI or use the pre-configured credentials if initialized:
- **Username**: `admin@college.edu`
- **Password**: `Admin@12345`

Or register any new email and password directly on the frontend registration modal.

---

## 5. Running Automated Backend Tests

To run unit and integration tests without starting external servers:
```powershell
cd backend
mvn test
```
The tests run using an in-memory database and verify:
- User registration, password hashing (BCrypt), and JWT token creation.
- Video file extension and MIME type validation.
- Job status lifecycle (QUEUED -> PROCESSING -> COMPLETED).
- Local storage adapter read, write, and secure path traversal prevention.
