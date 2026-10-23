# REST API Specification

Base URL: `/api`

All protected endpoints require the following HTTP Header:
```http
Authorization: Bearer <jwt_token>
```

---

## 1. Authentication Endpoints

### 1.1 Register New User
- **Method / Path**: `POST /auth/register`
- **Access**: Public
- **Request Body**:
```json
{
  "email": "user@college.edu",
  "password": "SecurePassword123",
  "fullName": "Jane Doe"
}
```
- **Response `201 Created`**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "type": "Bearer",
  "id": 1,
  "email": "user@college.edu",
  "fullName": "Jane Doe",
  "roles": ["ROLE_USER"]
}
```

### 1.2 Login
- **Method / Path**: `POST /auth/login`
- **Access**: Public
- **Request Body**:
```json
{
  "email": "user@college.edu",
  "password": "SecurePassword123"
}
```
- **Response `200 OK`**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "type": "Bearer",
  "id": 1,
  "email": "user@college.edu",
  "fullName": "Jane Doe",
  "roles": ["ROLE_USER"]
}
```

---

## 2. Video Job Management Endpoints

### 2.1 Upload Single Video
- **Method / Path**: `POST /videos/upload`
- **Access**: Authenticated (`ROLE_USER`)
- **Content-Type**: `multipart/form-data`
- **Form Parameters**:
  - `file`: Binary video file (`.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`)
  - `preset`: `LOW` (High Quality, 1080p, CRF 22), `MEDIUM` (Balanced, 720p, CRF 28), `HIGH` (Maximum Compression, 480p, CRF 32)
- **Response `202 Accepted`**:
```json
{
  "id": 101,
  "originalFileName": "sample_lecture.mp4",
  "status": "QUEUED",
  "originalSizeBytes": 157286400,
  "originalSizeFormatted": "150.00 MB",
  "compressedSizeBytes": null,
  "compressedSizeFormatted": null,
  "compressionRatioPercent": null,
  "preset": "MEDIUM",
  "targetResolution": "1280x720",
  "createdAt": "2026-10-23T11:00:00Z",
  "completedAt": null,
  "errorMessage": null
}
```

### 2.2 Batch Upload Multiple Videos
- **Method / Path**: `POST /videos/upload-batch`
- **Access**: Authenticated (`ROLE_USER`)
- **Content-Type**: `multipart/form-data`
- **Form Parameters**:
  - `files`: Array of binary video files
  - `preset`: `LOW`, `MEDIUM`, `HIGH`
- **Response `202 Accepted`**:
```json
{
  "totalUploaded": 3,
  "successfulJobs": [
    { "id": 101, "originalFileName": "part1.mp4", "status": "QUEUED" },
    { "id": 102, "originalFileName": "part2.mp4", "status": "QUEUED" },
    { "id": 103, "originalFileName": "part3.mp4", "status": "QUEUED" }
  ],
  "failedFiles": []
}
```

### 2.3 Get User Job History (Paginated)
- **Method / Path**: `GET /videos/jobs?page=0&size=20&status=ALL`
- **Access**: Authenticated (`ROLE_USER`)
- **Response `200 OK`**:
```json
{
  "content": [
    {
      "id": 101,
      "originalFileName": "sample_lecture.mp4",
      "status": "COMPLETED",
      "originalSizeBytes": 157286400,
      "originalSizeFormatted": "150.00 MB",
      "compressedSizeBytes": 47185920,
      "compressedSizeFormatted": "45.00 MB",
      "compressionRatioPercent": 70.0,
      "preset": "MEDIUM",
      "targetResolution": "1280x720",
      "createdAt": "2026-10-23T11:00:00Z",
      "completedAt": "2026-10-23T11:01:15Z",
      "errorMessage": null
    }
  ],
  "totalElements": 1,
  "totalPages": 1,
  "number": 0
}
```

### 2.4 Get Single Job Status
- **Method / Path**: `GET /videos/jobs/{jobId}`
- **Access**: Authenticated (Owner of job)
- **Response `200 OK`**: VideoJob details.

### 2.5 Secure Download Compressed Video
- **Method / Path**: `GET /videos/jobs/{jobId}/download`
- **Access**: Authenticated (Owner of job, verified server-side)
- **Response `200 OK`**: Video binary stream with headers:
  - `Content-Disposition: attachment; filename="compressed_sample_lecture.mp4"`
  - `Content-Type: video/mp4`

### 2.6 User Statistics Overview
- **Method / Path**: `GET /videos/stats`
- **Access**: Authenticated
- **Response `200 OK`**:
```json
{
  "totalJobs": 12,
  "completedJobs": 10,
  "queuedJobs": 1,
  "failedJobs": 1,
  "totalOriginalBytes": 2147483648,
  "totalCompressedBytes": 858993459,
  "totalSavedBytes": 1288490189,
  "totalSavedFormatted": "1.20 GB",
  "averageCompressionPercent": 60.0
}
```

---

## 3. Health & Readiness

### 3.1 Health Check
- **Method / Path**: `GET /health`
- **Access**: Public
- **Response `200 OK`**:
```json
{
  "status": "UP",
  "storageType": "local",
  "queueType": "local",
  "timestamp": "2026-10-23T11:00:00Z"
}
```
