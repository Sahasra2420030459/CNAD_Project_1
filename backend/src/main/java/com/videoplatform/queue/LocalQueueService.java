package com.videoplatform.queue;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

@Service("localQueueService")
public class LocalQueueService implements MessageQueueService {

    private static final Logger log = LoggerFactory.getLogger(LocalQueueService.class);

    private final LinkedBlockingQueue<JobQueueMessage> queue = new LinkedBlockingQueue<>();

    @Override
    public void enqueueJob(JobQueueMessage message) {
        log.info("Enqueuing job to Local In-Memory Queue: {}", message);
        queue.offer(message);
    }

    @Override
    public JobQueueMessage pollJob() {
        try {
            return queue.poll(100, TimeUnit.MILLISECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return null;
        }
    }

    @Override
    public int getQueueDepth() {
        return queue.size();
    }

    @Override
    public String getQueueType() {
        return "LOCAL_IN_MEMORY";
    }
}
