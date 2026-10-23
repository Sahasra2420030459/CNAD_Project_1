package com.videoplatform.dto;

import java.util.ArrayList;
import java.util.List;

public class BatchUploadResponse {

    private int totalUploaded;
    private List<VideoJobResponse> successfulJobs = new ArrayList<>();
    private List<FailedUploadItem> failedFiles = new ArrayList<>();

    public BatchUploadResponse() {}

    public BatchUploadResponse(int totalUploaded, List<VideoJobResponse> successfulJobs, List<FailedUploadItem> failedFiles) {
        this.totalUploaded = totalUploaded;
        this.successfulJobs = successfulJobs;
        this.failedFiles = failedFiles;
    }

    public static class FailedUploadItem {
        private String fileName;
        private String reason;

        public FailedUploadItem() {}

        public FailedUploadItem(String fileName, String reason) {
            this.fileName = fileName;
            this.reason = reason;
        }

        public String getFileName() {
            return fileName;
        }

        public void setFileName(String fileName) {
            this.fileName = fileName;
        }

        public String getReason() {
            return reason;
        }

        public void setReason(String reason) {
            this.reason = reason;
        }
    }

    public int getTotalUploaded() {
        return totalUploaded;
    }

    public void setTotalUploaded(int totalUploaded) {
        this.totalUploaded = totalUploaded;
    }

    public List<VideoJobResponse> getSuccessfulJobs() {
        return successfulJobs;
    }

    public void setSuccessfulJobs(List<VideoJobResponse> successfulJobs) {
        this.successfulJobs = successfulJobs;
    }

    public List<FailedUploadItem> getFailedFiles() {
        return failedFiles;
    }

    public void setFailedFiles(List<FailedUploadItem> failedFiles) {
        this.failedFiles = failedFiles;
    }
}
