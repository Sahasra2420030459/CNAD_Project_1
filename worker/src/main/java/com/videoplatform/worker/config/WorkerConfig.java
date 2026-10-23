package com.videoplatform.worker.config;

import com.videoplatform.worker.queue.AzureQueueService;
import com.videoplatform.worker.queue.LocalQueueService;
import com.videoplatform.worker.queue.MessageQueueService;
import com.videoplatform.worker.storage.AzureBlobStorageService;
import com.videoplatform.worker.storage.LocalStorageService;
import com.videoplatform.worker.storage.StorageService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class WorkerConfig {

    @Value("${storage.type:local}")
    private String storageType;

    @Value("${queue.type:local}")
    private String queueType;

    @Bean
    @Primary
    public StorageService storageService(LocalStorageService localStorageService,
                                         AzureBlobStorageService azureBlobStorageService) {
        if ("azure".equalsIgnoreCase(storageType)) {
            return azureBlobStorageService;
        }
        return localStorageService;
    }

    @Bean
    @Primary
    public MessageQueueService messageQueueService(LocalQueueService localQueueService,
                                                   AzureQueueService azureQueueService) {
        if ("azure".equalsIgnoreCase(queueType)) {
            return azureQueueService;
        }
        return localQueueService;
    }
}
