package com.videoplatform.worker.processor;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import jakarta.annotation.PostConstruct;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

@Component
public class FFmpegVideoCompressor {

    private static final Logger log = LoggerFactory.getLogger(FFmpegVideoCompressor.class);

    @Value("${worker.ffmpeg.path:ffmpeg}")
    private String ffmpegPath;

    @Value("${worker.ffmpeg.simulation-mode:auto}")
    private String simulationModeConfig;

    @Value("${worker.ffmpeg.timeout-seconds:1800}")
    private int timeoutSeconds;

    private boolean ffmpegAvailable = false;
    private boolean simulationActive = false;

    @PostConstruct
    public void init() {
        this.ffmpegAvailable = checkFFmpegAvailability();
        if ("true".equalsIgnoreCase(simulationModeConfig)) {
            this.simulationActive = true;
            log.info("FFmpeg simulation mode is FORCED ON by configuration.");
        } else if ("auto".equalsIgnoreCase(simulationModeConfig)) {
            this.simulationActive = !this.ffmpegAvailable;
            if (this.simulationActive) {
                log.warn("FFmpeg not found in system PATH. Auto-enabling SIMULATION MODE for local development.");
            } else {
                log.info("FFmpeg binary detected successfully at: {}. Real transcoding active.", ffmpegPath);
            }
        } else {
            this.simulationActive = false;
            log.info("FFmpeg simulation mode is OFF. Using system FFmpeg.");
        }
    }

    public CompressionResult compress(Path inputPath, Path outputPath, String preset) {
        long startTime = System.currentTimeMillis();

        if (simulationActive) {
            return simulateCompression(inputPath, outputPath, preset, startTime);
        }

        return executeRealFFmpeg(inputPath, outputPath, preset, startTime);
    }

    private CompressionResult executeRealFFmpeg(Path inputPath, Path outputPath, String preset, long startTime) {
        List<String> command = buildFFmpegCommand(inputPath, outputPath, preset);
        log.info("Executing FFmpeg command: {}", String.join(" ", command));

        StringBuilder stderrLog = new StringBuilder();

        try {
            ProcessBuilder pb = new ProcessBuilder(command);
            pb.redirectErrorStream(true);
            Process process = pb.start();

            // Read output stream in background to prevent buffer block
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    if (stderrLog.length() < 10000) {
                        stderrLog.append(line).append("\n");
                    }
                }
            }

            boolean finished = process.waitFor(timeoutSeconds, TimeUnit.SECONDS);
            long duration = System.currentTimeMillis() - startTime;

            if (!finished) {
                process.destroyForcibly();
                log.error("FFmpeg process timed out after {} seconds", timeoutSeconds);
                return CompressionResult.failed("FFmpeg process timed out after " + timeoutSeconds + " seconds", duration);
            }

            int exitCode = process.exitValue();
            if (exitCode != 0) {
                String errorExcerpt = stderrLog.substring(Math.max(0, stderrLog.length() - 800));
                log.error("FFmpeg exited with non-zero code {}. Output:\n{}", exitCode, errorExcerpt);
                return CompressionResult.failed("FFmpeg failed with exit code " + exitCode + ": " + errorExcerpt, duration);
            }

            if (!Files.exists(outputPath) || Files.size(outputPath) == 0) {
                return CompressionResult.failed("FFmpeg completed but output file is missing or empty.", duration);
            }

            long compressedSize = Files.size(outputPath);
            log.info("FFmpeg compression completed successfully in {} ms. Output size: {} bytes", duration, compressedSize);
            return CompressionResult.successful(outputPath, compressedSize, duration);

        } catch (Exception e) {
            long duration = System.currentTimeMillis() - startTime;
            log.error("Exception during FFmpeg execution: {}", e.getMessage(), e);
            return CompressionResult.failed("FFmpeg process execution failed: " + e.getMessage(), duration);
        }
    }

    private CompressionResult simulateCompression(Path inputPath, Path outputPath, String preset, long startTime) {
        try {
            long originalSize = Files.exists(inputPath) ? Files.size(inputPath) : 1024L;

            // Simulated compression ratios based on preset
            double reductionFactor = switch (preset.toUpperCase()) {
                case "HIGH" -> 0.40; // 60% reduction
                case "LOW" -> 0.75;  // 25% reduction
                default -> 0.55;     // 45% reduction (MEDIUM)
            };

            long simulatedSize = Math.max(128, (long) (originalSize * reductionFactor));

            // Generate simulated output file
            byte[] dummyData = new byte[(int) Math.min(simulatedSize, 65536)];
            for (int i = 0; i < dummyData.length; i++) {
                dummyData[i] = (byte) (i % 127);
            }
            Files.createDirectories(outputPath.getParent());
            Files.write(outputPath, dummyData);

            // Simulate realistic transcoding delay
            Thread.sleep(400);

            long duration = System.currentTimeMillis() - startTime;
            log.info("Simulated video compression completed in {} ms. Target size: {} bytes", duration, simulatedSize);
            return CompressionResult.successful(outputPath, simulatedSize, duration);

        } catch (Exception e) {
            long duration = System.currentTimeMillis() - startTime;
            return CompressionResult.failed("Simulated compression failed: " + e.getMessage(), duration);
        }
    }

    private List<String> buildFFmpegCommand(Path inputPath, Path outputPath, String preset) {
        List<String> command = new ArrayList<>();
        command.add(ffmpegPath);
        command.add("-y"); // overwrite output
        command.add("-i");
        command.add(inputPath.toAbsolutePath().toString());

        switch (preset.toUpperCase()) {
            case "LOW": // High quality 1080p, CRF 22, audio 192k
                command.add("-vf");
                command.add("scale=-2:1080");
                command.add("-c:v");
                command.add("libx264");
                command.add("-crf");
                command.add("22");
                command.add("-preset");
                command.add("fast");
                command.add("-c:a");
                command.add("aac");
                command.add("-b:a");
                command.add("192k");
                break;

            case "HIGH": // Maximum compression 480p, CRF 32, audio 96k
                command.add("-vf");
                command.add("scale=-2:480");
                command.add("-c:v");
                command.add("libx264");
                command.add("-crf");
                command.add("32");
                command.add("-preset");
                command.add("veryfast");
                command.add("-c:a");
                command.add("aac");
                command.add("-b:a");
                command.add("96k");
                break;

            case "MEDIUM":
            default: // Balanced 720p, CRF 28, audio 128k
                command.add("-vf");
                command.add("scale=-2:720");
                command.add("-c:v");
                command.add("libx264");
                command.add("-crf");
                command.add("28");
                command.add("-preset");
                command.add("fast");
                command.add("-c:a");
                command.add("aac");
                command.add("-b:a");
                command.add("128k");
                break;
        }

        // Faststart for web streaming optimization
        command.add("-movflags");
        command.add("+faststart");
        command.add(outputPath.toAbsolutePath().toString());

        return command;
    }

    private boolean checkFFmpegAvailability() {
        try {
            Process process = new ProcessBuilder(ffmpegPath, "-version").start();
            boolean finished = process.waitFor(3, TimeUnit.SECONDS);
            return finished && process.exitValue() == 0;
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isFFmpegAvailable() {
        return ffmpegAvailable;
    }

    public boolean isSimulationActive() {
        return simulationActive;
    }

    public void setSimulationActive(boolean simulationActive) {
        this.simulationActive = simulationActive;
    }
}
