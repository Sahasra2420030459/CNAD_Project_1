package com.videoplatform.worker.queue;

import com.videoplatform.worker.entity.JobStatus;
import com.videoplatform.worker.entity.VideoJob;
import com.videoplatform.worker.repository.VideoJobRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.concurrent.LinkedBlockingQueue;

@Service("workerLocalQueueService")
public class LocalQueueService implements MessageQueueService {

    private static final Logger log = LoggerFactory.getLogger(LocalQueueService.class);

    private final LinkedBlockingQueue<JobQueueMessage> queue = new LinkedBlockingQueue<>();
    private final VideoJobRepository videoJobRepository;

    public LocalQueueService(VideoJobRepository videoJobRepository) {
        this.videoJobRepository = videoJobRepository;
    }

    @Override
    public void enqueueJob(JobQueueMessage message) {
        queue.offer(message);
    }

    @Override
    public JobQueueMessage pollJob() {
        // First check in-memory queue
        JobQueueMessage msg = queue.poll();
        if (msg != null) {
            return msg;
        }

        // Database polling fallback for decoupled cross-process local mode
        try {
            List<VideoJob> pendingJobs = videoJobRepository.findByStatusOrderByCreatedAtAsc(JobStatus.QUEUED);
            if (!pendingJobs.isEmpty()) {
                VideoJob job = pendingJobs.get(0);
                return new JobQueueMessage(
                        job.getId(),
                        job.getUser().getId(),
                        job.getOriginalStoragePath(),
                        job.getOriginalFileName(),
                        job.getPreset()
                );
            }
        } catch (Exception e) {
            log.debug("Database queue poll idle: {}", e.getMessage());
        }

        return null;
    }

    @Override
    public int getQueueDepth() {
        return queue.size();
    }

    @Override
    public String getQueueType() {
        return "LOCAL_POLL_QUEUE";
    }
}
