package com.videoplatform.worker;

import com.videoplatform.worker.processor.CompressionResult;
import com.videoplatform.worker.processor.FFmpegVideoCompressor;
import org.springframework.test.util.ReflectionTestUtils;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;

public class WorkerVerificationTest {

    public static void main(String[] args) {
        System.out.println("=============================================================");
        System.out.println(" RUNNING WORKER TRANSCODING VERIFICATION SUITE");
        System.out.println("=============================================================");

        Path tempDir = null;
        int passed = 0;
        int failed = 0;

        try {
            tempDir = Files.createTempDirectory("verify-worker-");
            FFmpegVideoCompressor compressor = new FFmpegVideoCompressor();
            ReflectionTestUtils.setField(compressor, "ffmpegPath", "ffmpeg");
            ReflectionTestUtils.setField(compressor, "simulationModeConfig", "true");
            ReflectionTestUtils.setField(compressor, "timeoutSeconds", 10);
            compressor.init();

            // Test 1: MEDIUM Preset compression
            Path input1 = tempDir.resolve("sample1.mp4");
            byte[] originalContent1 = new byte[10000];
            Files.write(input1, originalContent1);

            Path output1 = tempDir.resolve("out_medium.mp4");
            CompressionResult res1 = compressor.compress(input1, output1, "MEDIUM");

            assertTrue(res1.isSuccess(), "Compression succeeds");
            assertTrue(Files.exists(output1), "Output file exists");
            assertTrue(res1.getCompressedSizeBytes() > 0, "Output size > 0");
            assertTrue(res1.getCompressedSizeBytes() < originalContent1.length, "Output smaller than input");
            System.out.println("  [PASS] FFmpegVideoCompressor MEDIUM preset compression");
            passed++;

            // Test 2: HIGH Preset compression
            Path input2 = tempDir.resolve("sample2.mp4");
            byte[] originalContent2 = new byte[20000];
            Files.write(input2, originalContent2);

            Path output2 = tempDir.resolve("out_high.mp4");
            CompressionResult res2 = compressor.compress(input2, output2, "HIGH");

            assertTrue(res2.isSuccess(), "Compression succeeds");
            assertTrue(Files.exists(output2), "Output file exists");
            assertTrue(res2.getCompressedSizeBytes() <= 10000, "High preset compresses by >= 50%");
            System.out.println("  [PASS] FFmpegVideoCompressor HIGH preset maximum compression");
            passed++;

        } catch (Throwable t) {
            System.err.println("  [FAIL] Worker test failed: " + t.getMessage());
            failed++;
        } finally {
            if (tempDir != null && Files.exists(tempDir)) {
                try {
                    Files.walk(tempDir).sorted(Comparator.reverseOrder()).map(Path::toFile).forEach(java.io.File::delete);
                } catch (IOException ignored) {}
            }
        }

        System.out.println("=============================================================");
        System.out.println(String.format("WORKER RESULTS: %d Passed | %d Failed", passed, failed));
        System.out.println("=============================================================");

        if (failed > 0) {
            System.exit(1);
        } else {
            System.out.println("ALL WORKER TESTS PASSED SUCCESSFULLY! (Verified)");
        }
    }

    private static void assertTrue(boolean condition, String msg) {
        if (!condition) {
            throw new AssertionError(msg + " -> Expected true, but was false");
        }
    }
}
