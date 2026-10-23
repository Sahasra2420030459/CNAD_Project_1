package com.videoplatform.controller;

import com.videoplatform.dto.BatchUploadResponse;
import com.videoplatform.dto.JobStatusResponse;
import com.videoplatform.dto.UserStatsResponse;
import com.videoplatform.dto.VideoJobResponse;
import com.videoplatform.entity.JobStatus;
import com.videoplatform.entity.VideoJob;
import com.videoplatform.security.UserPrincipal;
import com.videoplatform.service.VideoJobService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.core.io.Resource;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@RestController
@RequestMapping("/api/videos")
@Tag(name = "Video Processing Jobs", description = "Endpoints for uploading videos, managing compression jobs, status polling, and downloads")
@SecurityRequirement(name = "Bearer Authentication")
public class VideoJobController {

    private final VideoJobService videoJobService;

    public VideoJobController(VideoJobService videoJobService) {
        this.videoJobService = videoJobService;
    }

    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @Operation(summary = "Upload single video", description = "Uploads an individual video file and schedules an asynchronous FFmpeg compression job.")
    @ApiResponse(responseCode = "202", description = "Video upload accepted and queued for processing")
    public ResponseEntity<VideoJobResponse> uploadSingle(
            @Parameter(description = "Video binary file (.mp4, .mov, .avi, .mkv, .webm, up to 500MB)")
            @RequestParam("file") MultipartFile file,
            @Parameter(description = "Compression preset: LOW (1080p), MEDIUM (720p), HIGH (480p)")
            @RequestParam(value = "preset", defaultValue = "MEDIUM") String preset,
            @AuthenticationPrincipal UserPrincipal currentUser) {

        VideoJobResponse response = videoJobService.createJob(file, preset, currentUser.getId());
        return ResponseEntity.status(HttpStatus.ACCEPTED).body(response);
    }

    @PostMapping(value = "/upload-batch", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @Operation(summary = "Upload multiple videos in batch", description = "Uploads multiple video files simultaneously, creating individual asynchronous jobs.")
    @ApiResponse(responseCode = "202", description = "Batch upload processed with summary of queued and failed items")
    public ResponseEntity<BatchUploadResponse> uploadBatch(
            @Parameter(description = "List of video files to compress")
            @RequestParam("files") List<MultipartFile> files,
            @Parameter(description = "Compression preset for batch")
            @RequestParam(value = "preset", defaultValue = "MEDIUM") String preset,
            @AuthenticationPrincipal UserPrincipal currentUser) {

        BatchUploadResponse response = videoJobService.createBatchJobs(files, preset, currentUser.getId());
        return ResponseEntity.status(HttpStatus.ACCEPTED).body(response);
    }

    @GetMapping("/jobs")
    @Operation(summary = "Retrieve paginated user jobs", description = "Fetches job history for the authenticated user, optionally filtered by status.")
    @ApiResponse(responseCode = "200", description = "Paginated list of user video jobs")
    public ResponseEntity<Page<VideoJobResponse>> getJobs(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) String status,
            @AuthenticationPrincipal UserPrincipal currentUser) {

        JobStatus filterStatus = null;
        if (status != null && !status.equalsIgnoreCase("ALL") && !status.isBlank()) {
            try {
                filterStatus = JobStatus.valueOf(status.toUpperCase());
            } catch (IllegalArgumentException ignored) {}
        }

        PageRequest pageRequest = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
        Page<VideoJobResponse> jobs = videoJobService.getUserJobs(currentUser.getId(), pageRequest, filterStatus);
        return ResponseEntity.ok(jobs);
    }

    @GetMapping("/jobs/{id}")
    @Operation(summary = "Retrieve job by ID", description = "Returns full details of a video processing job. Enforces user ownership.")
    @ApiResponse(responseCode = "200", description = "Job details")
    @ApiResponse(responseCode = "403", description = "Access denied: job belongs to another user")
    @ApiResponse(responseCode = "404", description = "Job not found")
    public ResponseEntity<VideoJobResponse> getJob(
            @PathVariable Long id,
            @AuthenticationPrincipal UserPrincipal currentUser) {

        VideoJobResponse job = videoJobService.getJobById(id, currentUser.getId());
        return ResponseEntity.ok(job);
    }

    @GetMapping("/jobs/{id}/status")
    @Operation(summary = "Retrieve job status and progress", description = "Lightweight polling endpoint to retrieve current status (QUEUED, PROCESSING, COMPLETED, FAILED) and progress percentage.")
    @ApiResponse(responseCode = "200", description = "Current job status and progress")
    @ApiResponse(responseCode = "403", description = "Access denied")
    @ApiResponse(responseCode = "404", description = "Job not found")
    public ResponseEntity<JobStatusResponse> getJobStatus(
            @PathVariable Long id,
            @AuthenticationPrincipal UserPrincipal currentUser) {

        JobStatusResponse statusResponse = videoJobService.getJobStatus(id, currentUser.getId());
        return ResponseEntity.ok(statusResponse);
    }

    @PostMapping("/jobs/{id}/retry")
    @Operation(summary = "Retry eligible failed job", description = "Safely re-enqueues a job with FAILED status. Rejects active or completed jobs to prevent duplicate processing.")
    @ApiResponse(responseCode = "200", description = "Job successfully re-enqueued")
    @ApiResponse(responseCode = "400", description = "Job is not eligible for retry (e.g. not FAILED)")
    @ApiResponse(responseCode = "403", description = "Access denied")
    public ResponseEntity<VideoJobResponse> retryJob(
            @PathVariable Long id,
            @AuthenticationPrincipal UserPrincipal currentUser) {

        VideoJobResponse response = videoJobService.retryJob(id, currentUser.getId());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/jobs/{id}/download")
    @Operation(summary = "Download compressed video", description = "Securely streams the compressed video artifact after verifying user ownership and COMPLETED status.")
    @ApiResponse(responseCode = "200", description = "Binary video file stream")
    @ApiResponse(responseCode = "400", description = "Video processing is not yet completed")
    @ApiResponse(responseCode = "403", description = "Access denied")
    @ApiResponse(responseCode = "404", description = "Resource not found")
    public ResponseEntity<Resource> downloadCompressedVideo(
            @PathVariable Long id,
            @AuthenticationPrincipal UserPrincipal currentUser) {

        VideoJob job = videoJobService.getJobEntity(id, currentUser.getId());
        Resource resource = videoJobService.loadCompressedVideo(id, currentUser.getId());

        String filename = "compressed_" + job.getOriginalFileName();
        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + filename + "\"")
                .body(resource);
    }

    @GetMapping("/stats")
    @Operation(summary = "Retrieve user platform statistics", description = "Returns aggregated metrics including total jobs, queued, processing, completed, failed counts, and byte savings.")
    @ApiResponse(responseCode = "200", description = "User statistics overview")
    public ResponseEntity<UserStatsResponse> getStats(
            @AuthenticationPrincipal UserPrincipal currentUser) {

        UserStatsResponse stats = videoJobService.getUserStats(currentUser.getId());
        return ResponseEntity.ok(stats);
    }
}
