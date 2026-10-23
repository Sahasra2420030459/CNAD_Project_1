package com.videoplatform.worker.consumer;

import com.videoplatform.worker.entity.JobStatus;
import com.videoplatform.worker.entity.VideoJob;
import com.videoplatform.worker.processor.CompressionResult;
import com.videoplatform.worker.processor.FFmpegVideoCompressor;
import com.videoplatform.worker.queue.JobQueueMessage;
import com.videoplatform.worker.queue.MessageQueueService;
import com.videoplatform.worker.repository.VideoJobRepository;
import com.videoplatform.worker.storage.StorageService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

@Component
public class VideoJobConsumer {

    private static final Logger log = LoggerFactory.getLogger(VideoJobConsumer.class);

    private final MessageQueueService messageQueueService;
    private final VideoJobRepository videoJobRepository;
    private final StorageService storageService;
    private final FFmpegVideoCompressor ffmpegVideoCompressor;

    @Value("${worker.id:worker-node-1}")
    private String workerId;

    public VideoJobConsumer(MessageQueueService messageQueueService,
                            VideoJobRepository videoJobRepository,
                            StorageService storageService,
                            FFmpegVideoCompressor ffmpegVideoCompressor) {
        this.messageQueueService = messageQueueService;
        this.videoJobRepository = videoJobRepository;
        this.storageService = storageService;
        this.ffmpegVideoCompressor = ffmpegVideoCompressor;
    }

    @Scheduled(fixedDelayString = "${worker.poll-interval-ms:3000}")
    public void processNextJob() {
        JobQueueMessage message = messageQueueService.pollJob();
        if (message == null) {
            return;
        }

        log.info("Worker [{}] picked up job message: {}", workerId, message);

        Optional<VideoJob> optionalJob = videoJobRepository.findById(message.getJobId());
        if (optionalJob.isEmpty()) {
            log.warn("Job ID {} not found in database. Discarding message.", message.getJobId());
            return;
        }

        VideoJob job = optionalJob.get();
        if (job.getStatus() == JobStatus.COMPLETED) {
            log.info("Job ID {} is already completed. Skipping.", job.getId());
            return;
        }

        // Update status to PROCESSING
        job.setStatus(JobStatus.PROCESSING);
        job.setWorkerId(workerId);
        job.setErrorMessage(null);
        videoJobRepository.save(job);
        log.info("Job ID {} transition: QUEUED -> PROCESSING", job.getId());

        Path scratchDir = null;
        try {
            scratchDir = Files.createTempDirectory("video_transcode_" + job.getId() + "_");
            Path localInput = storageService.downloadToLocal(job.getOriginalStoragePath(), scratchDir);

            String outName = "compressed_" + UUID.randomUUID().toString() + ".mp4";
            Path localOutput = scratchDir.resolve(outName);

            CompressionResult result = ffmpegVideoCompressor.compress(localInput, localOutput, job.getPreset());

            if (result.isSuccess()) {
                String compressedStoragePath = storageService.uploadFromFile(localOutput, "compressed");

                job.setCompressedStoragePath(compressedStoragePath);
                job.setCompressedSizeBytes(result.getCompressedSizeBytes());

                long originalBytes = job.getOriginalSizeBytes();
                long compressedBytes = result.getCompressedSizeBytes();
                double ratio = 0.0;
                if (originalBytes > 0) {
                    ratio = ((double) (originalBytes - compressedBytes) / originalBytes) * 100.0;
                }
                job.setCompressionRatioPercent(Math.round(ratio * 10.0) / 10.0);
                job.setStatus(JobStatus.COMPLETED);
                job.setCompletedAt(Instant.now());
                log.info("Job ID {} successfully COMPLETED. Original: {}B, Compressed: {}B, Ratio: {}%",
                        job.getId(), originalBytes, compressedBytes, job.getCompressionRatioPercent());
            } else {
                job.setStatus(JobStatus.FAILED);
                job.setErrorMessage(result.getErrorMessage());
                log.error("Job ID {} FAILED: {}", job.getId(), result.getErrorMessage());
            }

        } catch (Exception e) {
            log.error("Unexpected worker error on Job ID {}: {}", job.getId(), e.getMessage(), e);
            job.setStatus(JobStatus.FAILED);
            job.setErrorMessage("Internal processing error: " + e.getMessage());
        } finally {
            videoJobRepository.save(job);
            cleanScratchDirectory(scratchDir);
        }
    }

    private void cleanScratchDirectory(Path dir) {
        if (dir != null && Files.exists(dir)) {
            try {
                Files.walk(dir)
                        .sorted(java.util.Comparator.reverseOrder())
                        .map(Path::toFile)
                        .forEach(java.io.File::delete);
            } catch (IOException e) {
                log.warn("Could not cleanly delete scratch directory: {}", dir, e);
            }
        }
    }
}
