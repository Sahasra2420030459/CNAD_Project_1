package com.videoplatform;

import com.videoplatform.dto.JobStatusResponse;
import com.videoplatform.dto.VideoJobResponse;
import com.videoplatform.entity.JobStatus;
import com.videoplatform.entity.ProcessingJob;
import com.videoplatform.entity.Role;
import com.videoplatform.entity.User;
import com.videoplatform.entity.Video;
import com.videoplatform.entity.VideoJob;
import com.videoplatform.exception.InvalidFileException;
import com.videoplatform.exception.StorageException;
import com.videoplatform.exception.UnauthorizedAccessException;
import com.videoplatform.service.VideoJobService;
import com.videoplatform.storage.LocalStorageService;
import org.springframework.core.io.Resource;
import org.springframework.mock.web.MockMultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;

public class CoreLogicVerificationTest {

    public static void main(String[] args) {
        System.out.println("=============================================================");
        System.out.println(" RUNNING CORE LOGIC AND STORAGE VERIFICATION SUITE");
        System.out.println("=============================================================");

        int passed = 0;
        int failed = 0;

        // 1. Preset & Resolution Tests
        try {
            assertEq("MEDIUM", VideoJobService.normalizePreset(null), "Default preset should be MEDIUM");
            assertEq("LOW", VideoJobService.normalizePreset("low"), "Preset lowercase normalized");
            assertEq("HIGH", VideoJobService.normalizePreset("HIGH"), "Preset HIGH normalized");
            assertEq("MEDIUM", VideoJobService.normalizePreset("invalid"), "Unknown preset falls back to MEDIUM");

            assertEq("1920x1080", VideoJobService.determineResolution("LOW"), "LOW preset resolution");
            assertEq("1280x720", VideoJobService.determineResolution("MEDIUM"), "MEDIUM preset resolution");
            assertEq("854x480", VideoJobService.determineResolution("HIGH"), "HIGH preset resolution");
            System.out.println("  [PASS] VideoJobService preset and resolution logic");
            passed++;
        } catch (Throwable t) {
            System.err.println("  [FAIL] Preset tests: " + t.getMessage());
            t.printStackTrace(System.err);
            failed++;
        }

        // 2. Byte Formatting Tests
        try {
            assertEq("1.50 MB", VideoJobResponse.formatBytes(1572864L), "Byte formatting MB");
            assertEq("1.00 GB", VideoJobResponse.formatBytes(1073741824L), "Byte formatting GB");
            assertEq("500.00 KB", VideoJobResponse.formatBytes(512000L), "Byte formatting KB");
            assertEq("-", VideoJobResponse.formatBytes(null), "Null byte formatting");
            System.out.println("  [PASS] VideoJobResponse byte formatting utility");
            passed++;
        } catch (Throwable t) {
            System.err.println("  [FAIL] Byte formatting tests: " + t.getMessage());
            failed++;
        }

        // 3. File Validation Tests
        try {
            VideoJobService service = new VideoJobService(null, null, null, null);

            // Bad extension
            MockMultipartFile exeFile = new MockMultipartFile("file", "malware.exe", "application/octet-stream", new byte[100]);
            assertThrows(InvalidFileException.class, () -> service.validateFile(exeFile), "Rejects .exe file");

            // Empty file
            MockMultipartFile emptyFile = new MockMultipartFile("file", "video.mp4", "video/mp4", new byte[0]);
            assertThrows(InvalidFileException.class, () -> service.validateFile(emptyFile), "Rejects empty file");

            // Valid video
            MockMultipartFile validMp4 = new MockMultipartFile("file", "lecture.mp4", "video/mp4", new byte[1024]);
            service.validateFile(validMp4); // should not throw

            // Valid MKV
            MockMultipartFile validMkv = new MockMultipartFile("file", "clip.mkv", "video/x-matroska", new byte[2048]);
            service.validateFile(validMkv); // should not throw

            System.out.println("  [PASS] VideoJobService MIME and extension validation");
            passed++;
        } catch (Throwable t) {
            System.err.println("  [FAIL] File validation tests: " + t.getMessage());
            failed++;
        }

        // 4. Local Storage & Path Traversal Tests
        Path tempDir = null;
        try {
            tempDir = Files.createTempDirectory("verify-storage-");
            LocalStorageService storage = new LocalStorageService(tempDir.toString());
            storage.init();

            // Store valid file
            MockMultipartFile file = new MockMultipartFile("file", "presentation.mp4", "video/mp4", "video content sample".getBytes());
            String storedPath = storage.store(file, "originals");
            assertTrue(storedPath.startsWith("originals/"), "Stored path starts with originals/");
            assertTrue(storedPath.endsWith(".mp4"), "Stored path ends with .mp4");

            // Load as resource
            Resource res = storage.loadAsResource(storedPath);
            assertTrue(res.exists(), "Stored resource exists");
            assertTrue(res.isReadable(), "Stored resource is readable");

            // Path traversal attempt
            MockMultipartFile badPathFile = new MockMultipartFile("file", "../../secret.txt", "text/plain", "data".getBytes());
            assertThrows(StorageException.class, () -> storage.store(badPathFile, "originals"), "Rejects path traversal");

            // Delete
            storage.delete(storedPath);
            assertThrows(StorageException.class, () -> storage.loadAsResource(storedPath), "Resource not found after delete");

            System.out.println("  [PASS] LocalStorageService storage, path traversal, and resource loading");
            passed++;
        } catch (Throwable t) {
            System.err.println("  [FAIL] Storage tests: " + t.getMessage());
            t.printStackTrace(System.err);
            failed++;
        } finally {
            if (tempDir != null && Files.exists(tempDir)) {
                try {
                    Files.walk(tempDir).sorted(Comparator.reverseOrder()).map(Path::toFile).forEach(java.io.File::delete);
                } catch (IOException ignored) {}
            }
        }

        // 5. VideoJob Entity & Status Lifecycle
        try {
            User user = new User("alice@college.edu", "hashed_pw", "Alice Student");
            user.setId(101L);

            VideoJob job = new VideoJob();
            job.setId(1L);
            job.setUser(user);
            job.setOriginalFileName("lab.mp4");
            job.setOriginalStoragePath("originals/uuid-lab.mp4");
            job.setOriginalSizeBytes(10000000L);
            job.setStatus(JobStatus.QUEUED);
            job.setPreset("MEDIUM");
            job.setTargetResolution("1280x720");

            assertEq(JobStatus.QUEUED, job.getStatus(), "Initial status is QUEUED");

            job.setStatus(JobStatus.PROCESSING);
            assertEq(JobStatus.PROCESSING, job.getStatus(), "Transitioned to PROCESSING");

            job.setCompressedSizeBytes(4000000L);
            double ratio = ((double) (job.getOriginalSizeBytes() - job.getCompressedSizeBytes()) / job.getOriginalSizeBytes()) * 100.0;
            job.setCompressionRatioPercent(Math.round(ratio * 10.0) / 10.0);
            job.setStatus(JobStatus.COMPLETED);

            assertEq(JobStatus.COMPLETED, job.getStatus(), "Transitioned to COMPLETED");
            assertEq(60.0, job.getCompressionRatioPercent(), "Compression ratio 60.0%");

            VideoJobResponse response = VideoJobResponse.fromEntity(job);
            assertEq(1L, response.getId(), "DTO matches entity ID");
            assertEq("/api/videos/jobs/1/download", response.getDownloadUrl(), "Download URL generated for COMPLETED job");

            System.out.println("  [PASS] VideoJob entity status lifecycle and DTO conversion");
            passed++;
        } catch (Throwable t) {
            System.err.println("  [FAIL] Entity tests: " + t.getMessage());
            failed++;
        }

        System.out.println("=============================================================");
        System.out.println(String.format("VERIFICATION RESULTS: %d Passed | %d Failed", passed, failed));
        System.out.println("=============================================================");

        if (failed > 0) {
            System.exit(1);
        } else {
            System.out.println("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!");
        }
    }

    private static void assertEq(Object expected, Object actual, String msg) {
        if (!java.util.Objects.equals(expected, actual)) {
            throw new AssertionError(msg + " -> Expected: " + expected + ", Actual: " + actual);
        }
    }

    private static void assertTrue(boolean condition, String msg) {
        if (!condition) {
            throw new AssertionError(msg + " -> Expected true, but was false");
        }
    }

    private static void assertThrows(Class<? extends Throwable> expected, Runnable block, String msg) {
        try {
            block.run();
            throw new AssertionError(msg + " -> Expected exception " + expected.getName() + " was NOT thrown");
        } catch (Throwable t) {
            if (!expected.isInstance(t)) {
                throw new AssertionError(msg + " -> Expected " + expected.getName() + ", but got " + t.getClass().getName() + ": " + t.getMessage());
            }
        }
    }
}
