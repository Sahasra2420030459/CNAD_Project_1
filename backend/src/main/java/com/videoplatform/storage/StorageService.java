package com.videoplatform.storage;

import org.springframework.core.io.Resource;
import org.springframework.web.multipart.MultipartFile;

import java.io.InputStream;

public interface StorageService {

    /**
     * Store an uploaded multipart file in the designated subfolder (e.g. "originals" or "compressed").
     * @return Unique storage path / blob identifier.
     */
    String store(MultipartFile file, String subDirectory);

    /**
     * Store raw input stream in storage.
     */
    String storeStream(InputStream inputStream, long size, String fileName, String contentType, String subDirectory);

    /**
     * Load stored file as a Spring Resource for streaming or downloading.
     */
    Resource loadAsResource(String storagePath);

    /**
     * Delete stored file.
     */
    void delete(String storagePath);

    /**
     * Get storage mechanism name.
     */
    String getStorageType();
}
