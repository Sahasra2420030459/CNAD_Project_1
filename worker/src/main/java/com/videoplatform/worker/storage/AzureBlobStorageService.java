package com.videoplatform.worker.storage;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.UUID;

@Service("workerAzureBlobStorageService")
public class AzureBlobStorageService implements StorageService {

    private static final Logger log = LoggerFactory.getLogger(AzureBlobStorageService.class);

    private final String connectionString;
    private final String containerName;
    private Object containerClient;

    public AzureBlobStorageService(
            @Value("${storage.azure.connection-string:}") String connectionString,
            @Value("${storage.azure.container-name:video-processing}") String containerName) {
        this.connectionString = connectionString;
        this.containerName = containerName;
    }

    private synchronized Object getContainerClient() {
        if (containerClient == null) {
            if (!StringUtils.hasText(connectionString)) {
                throw new IllegalStateException("Azure Storage Connection String is missing!");
            }
            try {
                Class<?> builderClass = Class.forName("com.azure.storage.blob.BlobServiceClientBuilder");
                Object builder = builderClass.getDeclaredConstructor().newInstance();
                Method connMethod = builderClass.getMethod("connectionString", String.class);
                connMethod.invoke(builder, connectionString);
                Method buildMethod = builderClass.getMethod("buildClient");
                Object serviceClient = buildMethod.invoke(builder);
                Method getContainerMethod = serviceClient.getClass().getMethod("getBlobContainerClient", String.class);
                containerClient = getContainerMethod.invoke(serviceClient, containerName);
            } catch (Exception e) {
                throw new RuntimeException("Failed to init Azure Blob client", e);
            }
        }
        return containerClient;
    }

    @Override
    public Path downloadToLocal(String storagePath, Path destinationDirectory) {
        try {
            Object container = getContainerClient();
            Method getBlobMethod = container.getClass().getMethod("getBlobClient", String.class);
            Object blobClient = getBlobMethod.invoke(container, storagePath);

            Path localTarget = destinationDirectory.resolve(UUID.randomUUID().toString() + "_download.mp4");
            Files.createDirectories(destinationDirectory);

            Method downloadToFileMethod = blobClient.getClass().getMethod("downloadToFile", String.class, boolean.class);
            downloadToFileMethod.invoke(blobClient, localTarget.toString(), true);
            log.info("Downloaded blob {} to local scratch: {}", storagePath, localTarget);
            return localTarget;
        } catch (Exception e) {
            throw new RuntimeException("Failed to download Azure Blob: " + storagePath, e);
        }
    }

    @Override
    public String uploadFromFile(Path filePath, String subDirectory) {
        try {
            String blobName = subDirectory + "/" + UUID.randomUUID().toString() + "_" + filePath.getFileName().toString();
            Object container = getContainerClient();
            Method getBlobMethod = container.getClass().getMethod("getBlobClient", String.class);
            Object blobClient = getBlobMethod.invoke(container, blobName);

            Method uploadFromFileMethod = blobClient.getClass().getMethod("uploadFromFile", String.class, boolean.class);
            uploadFromFileMethod.invoke(blobClient, filePath.toString(), true);
            log.info("Uploaded compressed video to Azure Blob: {}", blobName);
            return blobName;
        } catch (Exception e) {
            throw new RuntimeException("Failed to upload compressed file to Azure Blob: " + filePath, e);
        }
    }

    @Override
    public String getStorageType() {
        return "AZURE_BLOB";
    }
}
