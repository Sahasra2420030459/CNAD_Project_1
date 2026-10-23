package com.videoplatform.entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "video_jobs")
public class VideoJob {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(nullable = false)
    private String originalFileName;

    @Column(nullable = false, length = 500)
    private String originalStoragePath;

    @Column(length = 500)
    private String compressedStoragePath;

    @Column(nullable = false)
    private Long originalSizeBytes;

    private Long compressedSizeBytes;

    private Double compressionRatioPercent;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    private JobStatus status = JobStatus.QUEUED;

    @Column(nullable = false, length = 20)
    private String preset = "MEDIUM";

    @Column(length = 30)
    private String targetResolution;

    @Column(nullable = false)
    private Integer progress = 0;

    @Column(nullable = false)
    private Integer retryCount = 0;

    @Column(columnDefinition = "TEXT")
    private String errorMessage;

    @Column(length = 100)
    private String workerId;

    @Column(nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    private Instant updatedAt = Instant.now();

    private Instant completedAt;

    public VideoJob() {}

    @PreUpdate
    public void onUpdate() {
        this.updatedAt = Instant.now();
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public String getOriginalFileName() {
        return originalFileName;
    }

    public void setOriginalFileName(String originalFileName) {
        this.originalFileName = originalFileName;
    }

    public String getOriginalStoragePath() {
        return originalStoragePath;
    }

    public void setOriginalStoragePath(String originalStoragePath) {
        this.originalStoragePath = originalStoragePath;
    }

    public String getCompressedStoragePath() {
        return compressedStoragePath;
    }

    public void setCompressedStoragePath(String compressedStoragePath) {
        this.compressedStoragePath = compressedStoragePath;
    }

    public Long getOriginalSizeBytes() {
        return originalSizeBytes;
    }

    public void setOriginalSizeBytes(Long originalSizeBytes) {
        this.originalSizeBytes = originalSizeBytes;
    }

    public Long getCompressedSizeBytes() {
        return compressedSizeBytes;
    }

    public void setCompressedSizeBytes(Long compressedSizeBytes) {
        this.compressedSizeBytes = compressedSizeBytes;
    }

    public Double getCompressionRatioPercent() {
        return compressionRatioPercent;
    }

    public void setCompressionRatioPercent(Double compressionRatioPercent) {
        this.compressionRatioPercent = compressionRatioPercent;
    }

    public JobStatus getStatus() {
        return status;
    }

    public void setStatus(JobStatus status) {
        this.status = status;
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

    public String getWorkerId() {
        return workerId;
    }

    public void setWorkerId(String workerId) {
        this.workerId = workerId;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(Instant updatedAt) {
        this.updatedAt = updatedAt;
    }

    public Integer getProgress() {
        return progress;
    }

    public void setProgress(Integer progress) {
        this.progress = progress != null ? progress : 0;
    }

    public Integer getRetryCount() {
        return retryCount;
    }

    public void setRetryCount(Integer retryCount) {
        this.retryCount = retryCount != null ? retryCount : 0;
    }

    public Instant getCompletedAt() {
        return completedAt;
    }

    public void setCompletedAt(Instant completedAt) {
        this.completedAt = completedAt;
    }
}
