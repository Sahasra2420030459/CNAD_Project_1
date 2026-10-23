package com.videoplatform.config;

import com.videoplatform.storage.AzureBlobStorageService;
import com.videoplatform.storage.LocalStorageService;
import com.videoplatform.storage.StorageService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class StorageConfig {

    private static final Logger log = LoggerFactory.getLogger(StorageConfig.class);

    @Value("${storage.type:local}")
    private String storageType;

    @Bean
    @Primary
    public StorageService storageService(LocalStorageService localStorageService,
                                         AzureBlobStorageService azureBlobStorageService) {
        if ("azure".equalsIgnoreCase(storageType)) {
            log.info("Active Storage Adapter: AZURE_BLOB_STORAGE");
            return azureBlobStorageService;
        } else {
            log.info("Active Storage Adapter: LOCAL_DISK_STORAGE");
            return localStorageService;
        }
    }
}
