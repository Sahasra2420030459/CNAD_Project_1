# Architecture & System Design

## 1. Executive Summary

**The Cloud-Based Asynchronous Video Compression and Batch Processing Platform** is a distributed, enterprise-grade cloud native system designed to ingest, queue, transcode, and deliver videos asynchronously. It decouples high-throughput ingest operations from CPU-intensive video processing tasks using asynchronous messaging queues and scalable containerized background workers.

---

## 2. System Architecture Diagram

```
+-------------------------------------------------------------------------------+
|                                CLIENT TIER                                    |
|   React.js Web Application (Responsive, Batch Drag-Drop, Real-Time Polling)  |
|                   Deployed to: Azure Static Web Apps                          |
+---------------------------------------+---------------------------------------+
                                        | HTTPS / REST (JWT Auth)
                                        v
+-------------------------------------------------------------------------------+
|                              API BACKEND TIER                                 |
|     Java Spring Boot REST API (Spring Security, Spring Data JPA / Hibernate)  |
|                      Deployed to: Azure App Service                           |
|                                                                               |
|  - File Validation (MIME & Size)       - Job Record Creation (Status: QUEUED) |
|  - JWT Authentication & RBAC           - Storage Abstraction (Local / Azure)  |
|  - Batch Upload Management             - Queue Abstraction (Local / Azure)    |
+-------------------+-----------------------------------+-----------------------+
                    |                                   |
         Stores Blob|                          Dispatches Job
                    v                                   v
+------------------------------------+   +------------------------------------+
|           STORAGE TIER             |   |            QUEUE TIER              |
|  Azure Blob Storage (Cloud)        |   |  Azure Queue Storage (Cloud)       |
|  - Container: video-processing     |   |  - Queue: video-compression-jobs   |
|  OR Local Storage Adapter          |   |  OR Local In-Memory/DB Queue       |
+-------------------+----------------+   +------------------+-----------------+
                    ^                                       |
        Reads/Writes|                            Pulls Jobs |
                    |                                       v
+-------------------+-----------------------------------------------------------+
|                              WORKER POOL TIER                                 |
|          Background Java Transcoding Worker + FFmpeg Engine                   |
|                   Deployed to: Azure Container Apps                           |
|                                                                               |
|  - Pulls queued message                - Runs FFmpeg (CRF, preset, scale)     |
|  - Sets status: PROCESSING             - Computes output size & compression % |
|  - Downloads input blob to scratch     - Uploads compressed blob              |
|  - Sets status: COMPLETED / FAILED     - Logs execution stdout/stderr         |
+---------------------------------------+---------------------------------------+
                                        |
                            Persists Job Metadata & History
                                        v
+-------------------------------------------------------------------------------+
|                               DATABASE TIER                                   |
|   Azure Database for MySQL (Cloud Flexible Server) OR Local MySQL 8.0         |
|   - Tables: users, roles, user_roles, video_jobs, job_logs                    |
+-------------------------------------------------------------------------------+
```

---

## 3. Core Architectural Principles

### 3.1 Asynchronous Decoupling
Video compression is computationally intensive and non-deterministic in duration. If processed synchronously within an HTTP request:
- Client connections would time out (gateway timeouts, HTTP 504).
- Web application threads would saturate quickly under modest load.
- Batch uploads of multiple large videos would crash web instances.

By decoupling ingestion from processing:
1. The backend stores the file and enqueues a lightweight JSON job payload into the queue within milliseconds.
2. The client immediately receives a job ID with status `QUEUED` and polls the API (or receives SSE/WebSocket updates).
3. The worker processes tasks at its own rate, scaling horizontally via Azure Container Apps KEDA rules based on queue depth.

### 3.2 Pluggable Storage & Queue Abstractions (Local vs. Cloud)
To allow testing and local development without cloud costs or internet connectivity:
- **`StorageService` Interface**:
  - `LocalStorageService`: Persists to the local disk directory (`./uploads/originals`, `./uploads/compressed`).
  - `AzureBlobStorageService`: Uses Azure Blob Storage SDK (`BlobServiceClient`, `BlobContainerClient`).
- **`MessageQueueService` Interface**:
  - `LocalQueueService`: In-memory thread-safe blocking queue and database polling fallback.
  - `AzureQueueService`: Uses Azure Queue Storage SDK (`QueueClient`).
- Switching is controlled cleanly via `STORAGE_TYPE` and `QUEUE_TYPE` environment variables without touching any application code.

### 3.3 Security & Multi-Tenancy
- **Authentication**: Stateless JSON Web Tokens (JWT) signed via HMAC-SHA256.
- **Authorization**: Role-based access control (`ROLE_USER`, `ROLE_ADMIN`).
- **Data Isolation**: All video queries, job history, and download requests enforce tenant ownership checks (`user_id = principal.id`). Users cannot view or download other users' videos.
- **Secure File Ingestion**:
  - Extension whitelisting (`.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`).
  - MIME-type inspection.
  - Configurable maximum file size limit (default: 500MB per file).
  - Sanitization of stored filenames using UUIDs to prevent directory traversal attacks.

---

## 4. Job State Machine

```
      +-------------+
      | Video Upload|
      +------+------+
             |
             v
       [  QUEUED  ] --------(Enqueued in Azure Queue / Local Queue)
             |
             v
     (Worker picks job)
             |
             v
      [ PROCESSING ] --------(FFmpeg process executing)
             |
     +-------+-------+
     |               |
(Success)         (Error)
     |               |
     v               v
[ COMPLETED ]   [  FAILED  ]
     |               |
 Downloadable    Error logged
```

- **`QUEUED`**: The file has been validated and uploaded to storage; job message is in the queue.
- **`PROCESSING`**: A worker has acquired the message, downloaded the source file, and invoked the FFmpeg transcoding process.
- **`COMPLETED`**: FFmpeg finished with exit code 0; compressed video uploaded to storage; output size and compression percentage recorded.
- **`FAILED`**: Corrupt file, codec incompatibility, or worker crash; detailed error message preserved in database.
