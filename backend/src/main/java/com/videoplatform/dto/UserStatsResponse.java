package com.videoplatform.dto;

public class UserStatsResponse {

    private long totalJobs;
    private long queuedJobs;
    private long processingJobs;
    private long completedJobs;
    private long failedJobs;
    private long totalOriginalBytes;
    private long totalCompressedBytes;
    private long totalSavedBytes;
    private String totalSavedFormatted;
    private double averageCompressionPercent;

    public UserStatsResponse() {}

    public long getTotalJobs() {
        return totalJobs;
    }

    public void setTotalJobs(long totalJobs) {
        this.totalJobs = totalJobs;
    }

    public long getQueuedJobs() {
        return queuedJobs;
    }

    public void setQueuedJobs(long queuedJobs) {
        this.queuedJobs = queuedJobs;
    }

    public long getProcessingJobs() {
        return processingJobs;
    }

    public void setProcessingJobs(long processingJobs) {
        this.processingJobs = processingJobs;
    }

    public long getCompletedJobs() {
        return completedJobs;
    }

    public void setCompletedJobs(long completedJobs) {
        this.completedJobs = completedJobs;
    }

    public long getFailedJobs() {
        return failedJobs;
    }

    public void setFailedJobs(long failedJobs) {
        this.failedJobs = failedJobs;
    }

    public long getTotalOriginalBytes() {
        return totalOriginalBytes;
    }

    public void setTotalOriginalBytes(long totalOriginalBytes) {
        this.totalOriginalBytes = totalOriginalBytes;
    }

    public long getTotalCompressedBytes() {
        return totalCompressedBytes;
    }

    public void setTotalCompressedBytes(long totalCompressedBytes) {
        this.totalCompressedBytes = totalCompressedBytes;
    }

    public long getTotalSavedBytes() {
        return totalSavedBytes;
    }

    public void setTotalSavedBytes(long totalSavedBytes) {
        this.totalSavedBytes = totalSavedBytes;
    }

    public String getTotalSavedFormatted() {
        return totalSavedFormatted;
    }

    public void setTotalSavedFormatted(String totalSavedFormatted) {
        this.totalSavedFormatted = totalSavedFormatted;
    }

    public double getAverageCompressionPercent() {
        return averageCompressionPercent;
    }

    public void setAverageCompressionPercent(double averageCompressionPercent) {
        this.averageCompressionPercent = averageCompressionPercent;
    }
}
