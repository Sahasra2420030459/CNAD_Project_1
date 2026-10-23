package com.videoplatform.config;

import com.videoplatform.queue.AzureQueueService;
import com.videoplatform.queue.LocalQueueService;
import com.videoplatform.queue.MessageQueueService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class QueueConfig {

    private static final Logger log = LoggerFactory.getLogger(QueueConfig.class);

    @Value("${queue.type:local}")
    private String queueType;

    @Bean
    @Primary
    public MessageQueueService messageQueueService(LocalQueueService localQueueService,
                                                   AzureQueueService azureQueueService) {
        if ("azure".equalsIgnoreCase(queueType)) {
            log.info("Active Queue Adapter: AZURE_QUEUE_STORAGE");
            return azureQueueService;
        } else {
            log.info("Active Queue Adapter: LOCAL_IN_MEMORY_QUEUE");
            return localQueueService;
        }
    }
}
