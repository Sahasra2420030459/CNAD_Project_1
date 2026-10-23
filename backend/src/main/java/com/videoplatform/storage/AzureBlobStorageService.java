package com.videoplatform.storage;

import com.videoplatform.exception.StorageException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.InputStreamResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.InputStream;
import java.lang.reflect.Method;
import java.util.UUID;

/**
 * Azure Blob Storage Service.
 * Implemented with dynamic reflection binding to ensure seamless compilation
 * and local execution even when Azure SDK jars are not cached locally.
 */
@Service("azureBlobStorageService")
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
                throw new StorageException("Azure Storage Connection String is not configured!");
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

                Method existsMethod = containerClient.getClass().getMethod("exists");
                boolean exists = (boolean) existsMethod.invoke(containerClient);
                if (!exists) {
                    Method createMethod = containerClient.getClass().getMethod("create");
                    createMethod.invoke(containerClient);
                    log.info("Created Azure Blob Container: {}", containerName);
                }
            } catch (ClassNotFoundException e) {
                throw new StorageException("Azure Blob Storage SDK is not on the classpath. Add azure-storage-blob dependency.", e);
            } catch (Exception e) {
                throw new StorageException("Failed to initialize Azure Blob Storage client", e);
            }
        }
        return containerClient;
    }

    @Override
    public String store(MultipartFile file, String subDirectory) {
        if (file.isEmpty()) {
            throw new StorageException("Failed to store empty file to Azure Blob Storage.");
        }

        String originalFilename = StringUtils.cleanPath(file.getOriginalFilename() != null ? file.getOriginalFilename() : "video.mp4");
        String extension = "";
        int dotIndex = originalFilename.lastIndexOf('.');
        if (dotIndex >= 0) {
            extension = originalFilename.substring(dotIndex);
        }

        String blobName = subDirectory + "/" + UUID.randomUUID().toString() + extension;
        try {
            Object container = getContainerClient();
            Method getBlobMethod = container.getClass().getMethod("getBlobClient", String.class);
            Object blobClient = getBlobMethod.invoke(container, blobName);

            Method uploadMethod = blobClient.getClass().getMethod("upload", InputStream.class, long.class, boolean.class);
            try (InputStream is = file.getInputStream()) {
                uploadMethod.invoke(blobClient, is, file.getSize(), true);
            }
            log.info("Uploaded video to Azure Blob: {}", blobName);
            return blobName;
        } catch (Exception e) {
            throw new StorageException("Failed to upload file to Azure Blob Storage: " + blobName, e);
        }
    }

    @Override
    public String storeStream(InputStream inputStream, long size, String fileName, String contentType, String subDirectory) {
        String originalFilename = StringUtils.cleanPath(fileName);
        String extension = "";
        int dotIndex = originalFilename.lastIndexOf('.');
        if (dotIndex >= 0) {
            extension = originalFilename.substring(dotIndex);
        }

        String blobName = subDirectory + "/" + UUID.randomUUID().toString() + extension;
        try {
            Object container = getContainerClient();
            Method getBlobMethod = container.getClass().getMethod("getBlobClient", String.class);
            Object blobClient = getBlobMethod.invoke(container, blobName);

            Method uploadMethod = blobClient.getClass().getMethod("upload", InputStream.class, long.class, boolean.class);
            uploadMethod.invoke(blobClient, inputStream, size, true);
            log.info("Uploaded stream to Azure Blob: {}", blobName);
            return blobName;
        } catch (Exception e) {
            throw new StorageException("Failed to upload stream to Azure Blob Storage: " + blobName, e);
        }
    }

    @Override
    public Resource loadAsResource(String storagePath) {
        try {
            Object container = getContainerClient();
            Method getBlobMethod = container.getClass().getMethod("getBlobClient", String.class);
            Object blobClient = getBlobMethod.invoke(container, storagePath);

            Method existsMethod = blobClient.getClass().getMethod("exists");
            boolean exists = (boolean) existsMethod.invoke(blobClient);
            if (!exists) {
                throw new StorageException("Azure Blob does not exist at: " + storagePath);
            }

            Method openInputStreamMethod = blobClient.getClass().getMethod("openInputStream");
            InputStream inputStream = (InputStream) openInputStreamMethod.invoke(blobClient);
            return new InputStreamResource(inputStream);
        } catch (Exception e) {
            throw new StorageException("Failed to load Azure Blob resource: " + storagePath, e);
        }
    }

    @Override
    public void delete(String storagePath) {
        try {
            Object container = getContainerClient();
            Method getBlobMethod = container.getClass().getMethod("getBlobClient", String.class);
            Object blobClient = getBlobMethod.invoke(container, storagePath);

            Method existsMethod = blobClient.getClass().getMethod("exists");
            boolean exists = (boolean) existsMethod.invoke(blobClient);
            if (exists) {
                Method deleteMethod = blobClient.getClass().getMethod("delete");
                deleteMethod.invoke(blobClient);
                log.info("Deleted Azure Blob: {}", storagePath);
            }
        } catch (Exception e) {
            log.warn("Failed to delete Azure Blob: {}", storagePath, e);
        }
    }

    @Override
    public String getStorageType() {
        return "AZURE_BLOB";
    }
}
