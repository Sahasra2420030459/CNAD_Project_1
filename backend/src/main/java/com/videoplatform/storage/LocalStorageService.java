package com.videoplatform.storage;

import com.videoplatform.exception.StorageException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import jakarta.annotation.PostConstruct;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.nio.file.*;
import java.util.UUID;

@Service("localStorageService")
public class LocalStorageService implements StorageService {

    private static final Logger log = LoggerFactory.getLogger(LocalStorageService.class);

    private final Path rootLocation;

    public LocalStorageService(@Value("${storage.local.base-path:./uploads}") String basePath) {
        this.rootLocation = Paths.get(basePath).toAbsolutePath().normalize();
    }

    @PostConstruct
    public void init() {
        try {
            Files.createDirectories(this.rootLocation.resolve("originals"));
            Files.createDirectories(this.rootLocation.resolve("compressed"));
            log.info("Initialized local video storage directory at: {}", this.rootLocation);
        } catch (IOException e) {
            throw new StorageException("Could not initialize storage directory", e);
        }
    }

    @Override
    public String store(MultipartFile file, String subDirectory) {
        if (file.isEmpty()) {
            throw new StorageException("Failed to store empty file.");
        }

        String originalFilename = StringUtils.cleanPath(file.getOriginalFilename() != null ? file.getOriginalFilename() : "video.mp4");
        if (originalFilename.contains("..")) {
            throw new StorageException("Cannot store file with relative path outside current directory: " + originalFilename);
        }

        String extension = "";
        int dotIndex = originalFilename.lastIndexOf('.');
        if (dotIndex >= 0) {
            extension = originalFilename.substring(dotIndex);
        }

        String storedFilename = UUID.randomUUID().toString() + extension;
        Path targetDir = this.rootLocation.resolve(subDirectory).normalize();
        Path targetLocation = targetDir.resolve(storedFilename).normalize();

        try {
            Files.createDirectories(targetDir);
            try (InputStream inputStream = file.getInputStream()) {
                Files.copy(inputStream, targetLocation, StandardCopyOption.REPLACE_EXISTING);
            }
            log.info("Stored file locally at: {}", targetLocation);
            return subDirectory + "/" + storedFilename;
        } catch (IOException e) {
            throw new StorageException("Failed to store file " + originalFilename, e);
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

        String storedFilename = UUID.randomUUID().toString() + extension;
        Path targetDir = this.rootLocation.resolve(subDirectory).normalize();
        Path targetLocation = targetDir.resolve(storedFilename).normalize();

        try {
            Files.createDirectories(targetDir);
            Files.copy(inputStream, targetLocation, StandardCopyOption.REPLACE_EXISTING);
            log.info("Stored stream locally at: {}", targetLocation);
            return subDirectory + "/" + storedFilename;
        } catch (IOException e) {
            throw new StorageException("Failed to store stream as file " + fileName, e);
        }
    }

    @Override
    public Resource loadAsResource(String storagePath) {
        try {
            Path file = this.rootLocation.resolve(storagePath).normalize();
            if (!file.startsWith(this.rootLocation)) {
                throw new StorageException("Cannot access file outside designated storage directory");
            }

            Resource resource = new UrlResource(file.toUri());
            if (resource.exists() && resource.isReadable()) {
                return resource;
            } else {
                throw new StorageException("Could not read file at path: " + storagePath);
            }
        } catch (MalformedURLException e) {
            throw new StorageException("Could not read file: " + storagePath, e);
        }
    }

    @Override
    public void delete(String storagePath) {
        try {
            Path file = this.rootLocation.resolve(storagePath).normalize();
            if (file.startsWith(this.rootLocation)) {
                Files.deleteIfExists(file);
                log.info("Deleted local file: {}", file);
            }
        } catch (IOException e) {
            log.warn("Failed to delete local file: {}", storagePath, e);
        }
    }

    @Override
    public String getStorageType() {
        return "LOCAL_DISK";
    }

    public Path getRootLocation() {
        return rootLocation;
    }
}
