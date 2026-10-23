package com.videoplatform.worker.storage;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.*;
import java.util.UUID;

@Service("workerLocalStorageService")
public class LocalStorageService implements StorageService {

    private static final Logger log = LoggerFactory.getLogger(LocalStorageService.class);

    private final Path rootLocation;

    public LocalStorageService(@Value("${storage.local.base-path:./uploads}") String basePath) {
        this.rootLocation = Paths.get(basePath).toAbsolutePath().normalize();
    }

    @Override
    public Path downloadToLocal(String storagePath, Path destinationDirectory) {
        Path sourceFile = this.rootLocation.resolve(storagePath).normalize();
        if (!Files.exists(sourceFile)) {
            throw new RuntimeException("Original file not found on disk: " + sourceFile);
        }
        return sourceFile;
    }

    @Override
    public String uploadFromFile(Path filePath, String subDirectory) {
        String filename = UUID.randomUUID().toString() + "_" + filePath.getFileName().toString();
        Path targetDir = this.rootLocation.resolve(subDirectory).normalize();
        Path targetFile = targetDir.resolve(filename).normalize();

        try {
            Files.createDirectories(targetDir);
            Files.copy(filePath, targetFile, StandardCopyOption.REPLACE_EXISTING);
            log.info("Saved compressed file to local storage: {}", targetFile);
            return subDirectory + "/" + filename;
        } catch (IOException e) {
            throw new RuntimeException("Failed to upload file to local storage: " + targetFile, e);
        }
    }

    @Override
    public String getStorageType() {
        return "LOCAL_DISK";
    }
}
