package com.videoplatform.dto;

import com.videoplatform.entity.JobStatus;
import com.videoplatform.entity.VideoJob;

import java.time.Instant;

public class VideoJobResponse {

    private Long id;
    private String originalFileName;
    private JobStatus status;
    private Long originalSizeBytes;
    private String originalSizeFormatted;
    private Long compressedSizeBytes;
    private String compressedSizeFormatted;
    private Double compressionRatioPercent;
    private String preset;
    private String targetResolution;
    private String errorMessage;
    private Integer progress;
    private Integer retryCount;
    private Instant createdAt;
    private Instant completedAt;
    private String downloadUrl;

    public VideoJobResponse() {}

    public static VideoJobResponse fromEntity(VideoJob job) {
        VideoJobResponse res = new VideoJobResponse();
        res.setId(job.getId());
        res.setOriginalFileName(job.getOriginalFileName());
        res.setStatus(job.getStatus());
        res.setProgress(job.getProgress());
        res.setRetryCount(job.getRetryCount());
        res.setOriginalSizeBytes(job.getOriginalSizeBytes());
        res.setOriginalSizeFormatted(formatBytes(job.getOriginalSizeBytes()));
        res.setCompressedSizeBytes(job.getCompressedSizeBytes());
        res.setCompressedSizeFormatted(formatBytes(job.getCompressedSizeBytes()));
        res.setCompressionRatioPercent(job.getCompressionRatioPercent());
        res.setPreset(job.getPreset());
        res.setTargetResolution(job.getTargetResolution());
        res.setErrorMessage(job.getErrorMessage());
        res.setCreatedAt(job.getCreatedAt());
        res.setCompletedAt(job.getCompletedAt());

        if (job.getStatus() == JobStatus.COMPLETED) {
            res.setDownloadUrl("/api/videos/jobs/" + job.getId() + "/download");
        }
        return res;
    }

    public static VideoJobResponse fromEntity(com.videoplatform.entity.ProcessingJob job) {
        VideoJobResponse res = new VideoJobResponse();
        res.setId(job.getId());
        res.setOriginalFileName(job.getOriginalFileName());
        res.setStatus(job.getStatus());
        res.setProgress(job.getProgress());
        res.setRetryCount(job.getRetryCount());
        res.setOriginalSizeBytes(job.getOriginalSizeBytes());
        res.setOriginalSizeFormatted(formatBytes(job.getOriginalSizeBytes()));
        res.setCompressedSizeBytes(job.getCompressedSizeBytes());
        res.setCompressedSizeFormatted(formatBytes(job.getCompressedSizeBytes()));
        res.setCompressionRatioPercent(job.getCompressionRatioPercent());
        res.setPreset(job.getPreset());
        res.setTargetResolution(job.getTargetResolution());
        res.setErrorMessage(job.getErrorMessage());
        res.setCreatedAt(job.getCreatedAt());
        res.setCompletedAt(job.getCompletedAt());

        if (job.getStatus() == JobStatus.COMPLETED) {
            res.setDownloadUrl("/api/videos/jobs/" + job.getId() + "/download");
        }
        return res;
    }

    public static String formatBytes(Long bytes) {
        if (bytes == null || bytes <= 0) return "-";
        final String[] units = new String[] { "B", "KB", "MB", "GB", "TB" };
        int digitGroups = (int) (Math.log10(bytes) / Math.log10(1024));
        if (digitGroups >= units.length) digitGroups = units.length - 1;
        return String.format("%.2f %s", bytes / Math.pow(1024, digitGroups), units[digitGroups]);
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getOriginalFileName() {
        return originalFileName;
    }

    public void setOriginalFileName(String originalFileName) {
        this.originalFileName = originalFileName;
    }

    public JobStatus getStatus() {
        return status;
    }

    public void setStatus(JobStatus status) {
        this.status = status;
    }

    public Long getOriginalSizeBytes() {
        return originalSizeBytes;
    }

    public void setOriginalSizeBytes(Long originalSizeBytes) {
        this.originalSizeBytes = originalSizeBytes;
    }

    public String getOriginalSizeFormatted() {
        return originalSizeFormatted;
    }

    public void setOriginalSizeFormatted(String originalSizeFormatted) {
        this.originalSizeFormatted = originalSizeFormatted;
    }

    public Long getCompressedSizeBytes() {
        return compressedSizeBytes;
    }

    public void setCompressedSizeBytes(Long compressedSizeBytes) {
        this.compressedSizeBytes = compressedSizeBytes;
    }

    public String getCompressedSizeFormatted() {
        return compressedSizeFormatted;
    }

    public void setCompressedSizeFormatted(String compressedSizeFormatted) {
        this.compressedSizeFormatted = compressedSizeFormatted;
    }

    public Double getCompressionRatioPercent() {
        return compressionRatioPercent;
    }

    public void setCompressionRatioPercent(Double compressionRatioPercent) {
        this.compressionRatioPercent = compressionRatioPercent;
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

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
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

    public String getDownloadUrl() {
        return downloadUrl;
    }

    public void setDownloadUrl(String downloadUrl) {
        this.downloadUrl = downloadUrl;
    }
}
