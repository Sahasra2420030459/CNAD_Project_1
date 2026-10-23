package com.videoplatform.worker.storage;

import java.io.InputStream;
import java.nio.file.Path;

public interface StorageService {
    Path downloadToLocal(String storagePath, Path destinationDirectory);
    String uploadFromFile(Path filePath, String subDirectory);
    String getStorageType();
}
