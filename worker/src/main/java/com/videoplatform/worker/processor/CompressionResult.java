package com.videoplatform.worker.processor;

import java.nio.file.Path;

public class CompressionResult {

    private final boolean success;
    private final Path outputPath;
    private final long compressedSizeBytes;
    private final long durationMs;
    private final String errorMessage;

    public CompressionResult(boolean success, Path outputPath, long compressedSizeBytes, long durationMs, String errorMessage) {
        this.success = success;
        this.outputPath = outputPath;
        this.compressedSizeBytes = compressedSizeBytes;
        this.durationMs = durationMs;
        this.errorMessage = errorMessage;
    }

    public static CompressionResult successful(Path outputPath, long sizeBytes, long durationMs) {
        return new CompressionResult(true, outputPath, sizeBytes, durationMs, null);
    }

    public static CompressionResult failed(String errorMessage, long durationMs) {
        return new CompressionResult(false, null, 0L, durationMs, errorMessage);
    }

    public boolean isSuccess() {
        return success;
    }

    public Path getOutputPath() {
        return outputPath;
    }

    public long getCompressedSizeBytes() {
        return compressedSizeBytes;
    }

    public long getDurationMs() {
        return durationMs;
    }

    public String getErrorMessage() {
        return errorMessage;
    }
}
