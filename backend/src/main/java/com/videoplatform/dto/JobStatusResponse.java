package com.videoplatform.dto;

import com.videoplatform.entity.JobStatus;
import com.videoplatform.entity.ProcessingJob;
import com.videoplatform.entity.VideoJob;

import java.time.Instant;

/**
 * Lightweight response DTO for polling job status and progress.
 */
public class JobStatusResponse {

    private Long id;
    private JobStatus status;
    private Integer progress;
    private Integer retryCount;
    private String originalFileName;
    private String preset;
    private String targetResolution;
    private Instant createdAt;
    private Instant completedAt;
    private String errorMessage;
    private String downloadUrl;

    public JobStatusResponse() {}

    public static JobStatusResponse fromEntity(VideoJob job) {
        JobStatusResponse res = new JobStatusResponse();
        res.setId(job.getId());
        res.setStatus(job.getStatus());
        res.setProgress(job.getProgress());
        res.setRetryCount(job.getRetryCount());
        res.setOriginalFileName(job.getOriginalFileName());
        res.setPreset(job.getPreset());
        res.setTargetResolution(job.getTargetResolution());
        res.setCreatedAt(job.getCreatedAt());
        res.setCompletedAt(job.getCompletedAt());
        res.setErrorMessage(job.getErrorMessage());
        if (job.getStatus() == JobStatus.COMPLETED) {
            res.setDownloadUrl("/api/videos/jobs/" + job.getId() + "/download");
        }
        return res;
    }

    public static JobStatusResponse fromEntity(ProcessingJob job) {
        JobStatusResponse res = new JobStatusResponse();
        res.setId(job.getId());
        res.setStatus(job.getStatus());
        res.setProgress(job.getProgress());
        res.setRetryCount(job.getRetryCount());
        res.setOriginalFileName(job.getOriginalFileName());
        res.setPreset(job.getPreset());
        res.setTargetResolution(job.getTargetResolution());
        res.setCreatedAt(job.getCreatedAt());
        res.setCompletedAt(job.getCompletedAt());
        res.setErrorMessage(job.getErrorMessage());
        if (job.getStatus() == JobStatus.COMPLETED) {
            res.setDownloadUrl("/api/videos/jobs/" + job.getId() + "/download");
        }
        return res;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public JobStatus getStatus() {
        return status;
    }

    public void setStatus(JobStatus status) {
        this.status = status;
    }

    public Integer getProgress() {
        return progress;
    }

    public void setProgress(Integer progress) {
        this.progress = progress;
    }

    public Integer getRetryCount() {
        return retryCount;
    }

    public void setRetryCount(Integer retryCount) {
        this.retryCount = retryCount;
    }

    public String getOriginalFileName() {
        return originalFileName;
    }

    public void setOriginalFileName(String originalFileName) {
        this.originalFileName = originalFileName;
    }

    public String getPreset() {
        return preset;
    }

    public void setPreset(String preset) {
        this.preset = preset;
    }

    public String getTargetResolution() {
        return targetResolution;
    }

    public void setTargetResolution(String targetResolution) {
        this.targetResolution = targetResolution;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }

    public Instant getCompletedAt() {
        return completedAt;
    }

    public void setCompletedAt(Instant completedAt) {
        this.completedAt = completedAt;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public String getDownloadUrl() {
        return downloadUrl;
    }

    public void setDownloadUrl(String downloadUrl) {
        this.downloadUrl = downloadUrl;
    }
}
