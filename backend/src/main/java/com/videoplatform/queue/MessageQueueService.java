package com.videoplatform.queue;

public interface MessageQueueService {

    /**
     * Enqueue a new video compression job payload.
     */
    void enqueueJob(JobQueueMessage message);

    /**
     * Poll a job message from the queue, or return null if empty.
     */
    JobQueueMessage pollJob();

    /**
     * Current queue length approximation.
     */
    int getQueueDepth();

    /**
     * Queue implementation type name.
     */
    String getQueueType();
}
