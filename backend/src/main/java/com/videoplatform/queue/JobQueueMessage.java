package com.videoplatform.queue;

import java.io.Serializable;

public class JobQueueMessage implements Serializable {

    private static final long serialVersionUID = 1L;

    private Long jobId;
    private Long userId;
    private String originalStoragePath;
    private String originalFileName;
    private String preset;

    public JobQueueMessage() {}

    public JobQueueMessage(Long jobId, Long userId, String originalStoragePath, String originalFileName, String preset) {
        this.jobId = jobId;
        this.userId = userId;
        this.originalStoragePath = originalStoragePath;
        this.originalFileName = originalFileName;
        this.preset = preset;
    }

    public Long getJobId() {
        return jobId;
    }

    public void setJobId(Long jobId) {
        this.jobId = jobId;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getOriginalStoragePath() {
        return originalStoragePath;
    }

    public void setOriginalStoragePath(String originalStoragePath) {
        this.originalStoragePath = originalStoragePath;
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

    @Override
    public String toString() {
        return "JobQueueMessage{" +
                "jobId=" + jobId +
                ", userId=" + userId +
                ", originalFileName='" + originalFileName + '\'' +
                ", preset='" + preset + '\'' +
                '}';
    }
}
