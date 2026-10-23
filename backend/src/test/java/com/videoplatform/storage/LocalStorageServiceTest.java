package com.videoplatform.storage;

import com.videoplatform.exception.StorageException;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.core.io.Resource;
import org.springframework.mock.web.MockMultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;

import static org.junit.jupiter.api.Assertions.*;

public class LocalStorageServiceTest {

    private Path tempDir;
    private LocalStorageService storageService;

    @BeforeEach
    void setUp() throws IOException {
        tempDir = Files.createTempDirectory("test-video-storage-");
        storageService = new LocalStorageService(tempDir.toString());
        storageService.init();
    }

    @AfterEach
    void tearDown() throws IOException {
        if (Files.exists(tempDir)) {
            Files.walk(tempDir)
                    .sorted(Comparator.reverseOrder())
                    .map(Path::toFile)
                    .forEach(java.io.File::delete);
        }
    }

    @Test
    void testStoreAndLoadFile() throws IOException {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "test_lecture.mp4",
                "video/mp4",
                "Sample video binary content".getBytes()
        );

        String storedPath = storageService.store(file, "originals");
        assertNotNull(storedPath);
        assertTrue(storedPath.startsWith("originals/"));
        assertTrue(storedPath.endsWith(".mp4"));

        Resource resource = storageService.loadAsResource(storedPath);
        assertTrue(resource.exists());
        assertTrue(resource.isReadable());
        assertEquals("Sample video binary content", new String(resource.getInputStream().readAllBytes()));
    }

    @Test
    void testPathTraversalThrowsException() {
        MockMultipartFile maliciousFile = new MockMultipartFile(
                "file",
                "../../etc/passwd",
                "text/plain",
                "malicious".getBytes()
        );

        assertThrows(StorageException.class, () -> {
            storageService.store(maliciousFile, "originals");
        });
    }

    @Test
    void testEmptyFileThrowsException() {
        MockMultipartFile emptyFile = new MockMultipartFile(
                "file",
                "empty.mp4",
                "video/mp4",
                new byte[0]
        );

        assertThrows(StorageException.class, () -> {
            storageService.store(emptyFile, "originals");
        });
    }

    @Test
    void testDeleteFile() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "sample.mp4",
                "video/mp4",
                "video payload".getBytes()
        );

        String storedPath = storageService.store(file, "originals");
        Resource resource = storageService.loadAsResource(storedPath);
        assertTrue(resource.exists());

        storageService.delete(storedPath);
        assertThrows(StorageException.class, () -> storageService.loadAsResource(storedPath));
    }
}
