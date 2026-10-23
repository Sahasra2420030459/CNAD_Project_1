package com.videoplatform.worker.queue;

public interface MessageQueueService {
    void enqueueJob(JobQueueMessage message);
    JobQueueMessage pollJob();
    int getQueueDepth();
    String getQueueType();
}
