package com.videoplatform.service;

import com.videoplatform.dto.BatchUploadResponse;
import com.videoplatform.dto.JobStatusResponse;
import com.videoplatform.dto.UserStatsResponse;
import com.videoplatform.dto.VideoJobResponse;
import com.videoplatform.entity.JobStatus;
import com.videoplatform.entity.ProcessingJob;
import com.videoplatform.entity.User;
import com.videoplatform.entity.Video;
import com.videoplatform.entity.VideoJob;
import com.videoplatform.exception.InvalidFileException;
import com.videoplatform.exception.ResourceNotFoundException;
import com.videoplatform.exception.UnauthorizedAccessException;
import com.videoplatform.queue.JobQueueMessage;
import com.videoplatform.queue.MessageQueueService;
import com.videoplatform.repository.ProcessingJobRepository;
import com.videoplatform.repository.UserRepository;
import com.videoplatform.repository.VideoJobRepository;
import com.videoplatform.repository.VideoRepository;
import com.videoplatform.storage.StorageService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.util.*;

@Service
public class VideoJobService {

    private static final Logger log = LoggerFactory.getLogger(VideoJobService.class);

    private static final long MAX_FILE_SIZE = 500L * 1024L * 1024L; // 500MB
    private static final Set<String> ALLOWED_EXTENSIONS = Set.of(
            "mp4", "avi", "mov", "mkv", "webm", "flv", "wmv", "m4v"
    );

    private final VideoJobRepository videoJobRepository;
    private final UserRepository userRepository;
    private final StorageService storageService;
    private final MessageQueueService messageQueueService;
    private final VideoRepository videoRepository;
    private final ProcessingJobRepository processingJobRepository;

    public VideoJobService(VideoJobRepository videoJobRepository,
                           UserRepository userRepository,
                           StorageService storageService,
                           MessageQueueService messageQueueService) {
        this(videoJobRepository, userRepository, storageService, messageQueueService, null, null);
    }

    @Autowired
    public VideoJobService(VideoJobRepository videoJobRepository,
                           UserRepository userRepository,
                           StorageService storageService,
                           MessageQueueService messageQueueService,
                           @Autowired(required = false) VideoRepository videoRepository,
                           @Autowired(required = false) ProcessingJobRepository processingJobRepository) {
        this.videoJobRepository = videoJobRepository;
        this.userRepository = userRepository;
        this.storageService = storageService;
        this.messageQueueService = messageQueueService;
        this.videoRepository = videoRepository;
        this.processingJobRepository = processingJobRepository;
    }

    @Transactional
    public VideoJobResponse createJob(MultipartFile file, String preset, Long userId) {
        validateFile(file);

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + userId));

        String sanitizedOriginalName = StringUtils.cleanPath(file.getOriginalFilename() != null ? file.getOriginalFilename() : "video.mp4");
        String normalizedPreset = normalizePreset(preset);
        String targetResolution = determineResolution(normalizedPreset);

        // Store original video
        String storedPath = storageService.store(file, "originals");

        // Persist Video entity if repository configured
        Video savedVideo = null;
        if (videoRepository != null) {
            Video video = new Video(user, sanitizedOriginalName, storedPath, file.getSize(), file.getContentType());
            savedVideo = videoRepository.save(video);
        }

        // Create unified VideoJob database entity
        VideoJob job = new VideoJob();
        job.setUser(user);
        job.setOriginalFileName(sanitizedOriginalName);
        job.setOriginalStoragePath(storedPath);
        job.setOriginalSizeBytes(file.getSize());
        job.setStatus(JobStatus.QUEUED);
        job.setProgress(0);
        job.setRetryCount(0);
        job.setPreset(normalizedPreset);
        job.setTargetResolution(targetResolution);

        VideoJob savedJob = videoJobRepository.save(job);

        // Persist ProcessingJob entity if repository configured
        if (processingJobRepository != null) {
            ProcessingJob processingJob = new ProcessingJob();
            processingJob.setUser(user);
            processingJob.setVideo(savedVideo);
            processingJob.setOriginalFileName(sanitizedOriginalName);
            processingJob.setOriginalStoragePath(storedPath);
            processingJob.setOriginalSizeBytes(file.getSize());
            processingJob.setStatus(JobStatus.QUEUED);
            processingJob.setProgress(0);
            processingJob.setRetryCount(0);
            processingJob.setPreset(normalizedPreset);
            processingJob.setTargetResolution(targetResolution);
            processingJobRepository.save(processingJob);
        }

        log.info("Created VideoJob ID: {} for user: {} with preset: {}", savedJob.getId(), user.getEmail(), normalizedPreset);

        // Enqueue async job
        JobQueueMessage queueMessage = new JobQueueMessage(
                savedJob.getId(),
                user.getId(),
                savedJob.getOriginalStoragePath(),
                savedJob.getOriginalFileName(),
                savedJob.getPreset()
        );
        messageQueueService.enqueueJob(queueMessage);

        return VideoJobResponse.fromEntity(savedJob);
    }

    @Transactional
    public BatchUploadResponse createBatchJobs(List<MultipartFile> files, String preset, Long userId) {
        if (files == null || files.isEmpty()) {
            throw new InvalidFileException("Batch upload requires at least one video file.");
        }

        List<VideoJobResponse> successfulJobs = new ArrayList<>();
        List<BatchUploadResponse.FailedUploadItem> failedFiles = new ArrayList<>();

        for (MultipartFile file : files) {
            String fileName = file.getOriginalFilename() != null ? file.getOriginalFilename() : "unknown";
            try {
                VideoJobResponse response = createJob(file, preset, userId);
                successfulJobs.add(response);
            } catch (Exception e) {
                log.warn("Failed to process batch item {}: {}", fileName, e.getMessage());
                failedFiles.add(new BatchUploadResponse.FailedUploadItem(fileName, e.getMessage()));
            }
        }

        return new BatchUploadResponse(successfulJobs.size(), successfulJobs, failedFiles);
    }

    @Transactional
    public VideoJobResponse retryJob(Long jobId, Long userId) {
        VideoJob job = videoJobRepository.findById(jobId)
                .orElseThrow(() -> new ResourceNotFoundException("Video job not found with id: " + jobId));

        if (!job.getUser().getId().equals(userId)) {
            throw new UnauthorizedAccessException("You do not have permission to retry this job.");
        }

        if (job.getStatus() != JobStatus.FAILED) {
            throw new InvalidFileException("Only FAILED jobs are eligible for retry. Current status: " + job.getStatus());
        }

        job.setStatus(JobStatus.QUEUED);
        job.setProgress(0);
        job.setRetryCount(job.getRetryCount() != null ? job.getRetryCount() + 1 : 1);
        job.setErrorMessage(null);
        job.setCompressedStoragePath(null);
        job.setCompressedSizeBytes(null);
        job.setCompressionRatioPercent(null);
        job.setCompletedAt(null);
        job.setWorkerId(null);

        VideoJob savedJob = videoJobRepository.save(job);
        log.info("Retrying VideoJob ID: {} (attempt #{}) for user: {}", savedJob.getId(), savedJob.getRetryCount(), userId);

        JobQueueMessage queueMessage = new JobQueueMessage(
                savedJob.getId(),
                userId,
                savedJob.getOriginalStoragePath(),
                savedJob.getOriginalFileName(),
                savedJob.getPreset()
        );
        messageQueueService.enqueueJob(queueMessage);

        return VideoJobResponse.fromEntity(savedJob);
    }

    @Transactional(readOnly = true)
    public JobStatusResponse getJobStatus(Long jobId, Long userId) {
        VideoJob job = videoJobRepository.findById(jobId)
                .orElseThrow(() -> new ResourceNotFoundException("Video job not found with id: " + jobId));

        if (!job.getUser().getId().equals(userId)) {
            throw new UnauthorizedAccessException("You do not have permission to view this job status.");
        }

        return JobStatusResponse.fromEntity(job);
    }

    @Transactional(readOnly = true)
    public Page<VideoJobResponse> getUserJobs(Long userId, Pageable pageable, JobStatus filterStatus) {
        Page<VideoJob> page;
        if (filterStatus != null) {
            page = videoJobRepository.findByUserIdAndStatus(userId, filterStatus, pageable);
        } else {
            page = videoJobRepository.findByUserId(userId, pageable);
        }
        return page.map(VideoJobResponse::fromEntity);
    }

    @Transactional(readOnly = true)
    public VideoJobResponse getJobById(Long jobId, Long userId) {
        VideoJob job = videoJobRepository.findById(jobId)
                .orElseThrow(() -> new ResourceNotFoundException("Video job not found with id: " + jobId));

        if (!job.getUser().getId().equals(userId)) {
            throw new UnauthorizedAccessException("You do not have permission to view this job.");
        }

        return VideoJobResponse.fromEntity(job);
    }

    @Transactional(readOnly = true)
    public Resource loadCompressedVideo(Long jobId, Long userId) {
        VideoJob job = videoJobRepository.findById(jobId)
                .orElseThrow(() -> new ResourceNotFoundException("Video job not found with id: " + jobId));

        if (!job.getUser().getId().equals(userId)) {
            throw new UnauthorizedAccessException("You do not have permission to download this video.");
        }

        if (job.getStatus() != JobStatus.COMPLETED) {
            throw new InvalidFileException("Video compression has not completed yet. Current status: " + job.getStatus());
        }

        if (!StringUtils.hasText(job.getCompressedStoragePath())) {
            throw new ResourceNotFoundException("Compressed video path is missing.");
        }

        return storageService.loadAsResource(job.getCompressedStoragePath());
    }

    @Transactional(readOnly = true)
    public VideoJob getJobEntity(Long jobId, Long userId) {
        VideoJob job = videoJobRepository.findById(jobId)
                .orElseThrow(() -> new ResourceNotFoundException("Video job not found with id: " + jobId));

        if (!job.getUser().getId().equals(userId)) {
            throw new UnauthorizedAccessException("You do not have permission to access this job.");
        }
        return job;
    }

    @Transactional(readOnly = true)
    public UserStatsResponse getUserStats(Long userId) {
        UserStatsResponse stats = new UserStatsResponse();
        stats.setTotalJobs(videoJobRepository.countByUserId(userId));
        stats.setQueuedJobs(videoJobRepository.countByUserIdAndStatus(userId, JobStatus.QUEUED));
        stats.setProcessingJobs(videoJobRepository.countByUserIdAndStatus(userId, JobStatus.PROCESSING));
        stats.setCompletedJobs(videoJobRepository.countByUserIdAndStatus(userId, JobStatus.COMPLETED));
        stats.setFailedJobs(videoJobRepository.countByUserIdAndStatus(userId, JobStatus.FAILED));

        Long totalOriginal = videoJobRepository.sumOriginalSizeBytesByUserId(userId);
        Long totalCompressed = videoJobRepository.sumCompressedSizeBytesByUserId(userId);

        long original = totalOriginal != null ? totalOriginal : 0L;
        long compressed = totalCompressed != null ? totalCompressed : 0L;
        long saved = Math.max(0, original - compressed);

        stats.setTotalOriginalBytes(original);
        stats.setTotalCompressedBytes(compressed);
        stats.setTotalSavedBytes(saved);
        stats.setTotalSavedFormatted(VideoJobResponse.formatBytes(saved));

        if (original > 0 && stats.getCompletedJobs() > 0) {
            double avgPercent = ((double) saved / original) * 100.0;
            stats.setAverageCompressionPercent(Math.round(avgPercent * 10.0) / 10.0);
        } else {
            stats.setAverageCompressionPercent(0.0);
        }

        return stats;
    }

    public void validateFile(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new InvalidFileException("Uploaded file cannot be empty.");
        }

        if (file.getSize() > MAX_FILE_SIZE) {
            throw new InvalidFileException("File size exceeds 500MB maximum limit.");
        }

        String filename = file.getOriginalFilename();
        if (filename == null || !filename.contains(".")) {
            throw new InvalidFileException("File name must contain an extension.");
        }

        String extension = filename.substring(filename.lastIndexOf('.') + 1).toLowerCase();
        if (!ALLOWED_EXTENSIONS.contains(extension)) {
            throw new InvalidFileException("Unsupported video extension: '." + extension +
                    "'. Allowed formats: " + ALLOWED_EXTENSIONS);
        }

        String contentType = file.getContentType();
        if (contentType != null && !contentType.toLowerCase().startsWith("video/") &&
            !contentType.equalsIgnoreCase("application/octet-stream")) {
            throw new InvalidFileException("File is not recognized as a video format (MIME: " + contentType + ")");
        }
    }

    public static String normalizePreset(String preset) {
        if (preset == null) return "MEDIUM";
        String upper = preset.trim().toUpperCase();
        if (upper.equals("LOW") || upper.equals("MEDIUM") || upper.equals("HIGH")) {
            return upper;
        }
        return "MEDIUM";
    }

    public static String determineResolution(String preset) {
        return switch (preset) {
            case "LOW" -> "1920x1080";
            case "HIGH" -> "854x480";
            default -> "1280x720";
        };
    }
}
