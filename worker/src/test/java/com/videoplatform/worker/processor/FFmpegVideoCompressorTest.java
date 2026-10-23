package com.videoplatform.worker.processor;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;

import static org.junit.jupiter.api.Assertions.*;

class FFmpegVideoCompressorTest {

    private Path tempDir;
    private FFmpegVideoCompressor compressor;

    @BeforeEach
    void setUp() throws IOException {
        tempDir = Files.createTempDirectory("worker-test-");
        compressor = new FFmpegVideoCompressor();
        ReflectionTestUtils.setField(compressor, "ffmpegPath", "ffmpeg");
        ReflectionTestUtils.setField(compressor, "simulationModeConfig", "true");
        ReflectionTestUtils.setField(compressor, "timeoutSeconds", 10);
        compressor.init();
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
    void testSimulationCompressionMediumPreset() throws IOException {
        Path input = tempDir.resolve("sample.mp4");
        byte[] originalContent = new byte[10000];
        Files.write(input, originalContent);

        Path output = tempDir.resolve("output_medium.mp4");
        CompressionResult result = compressor.compress(input, output, "MEDIUM");

        assertTrue(result.isSuccess());
        assertTrue(Files.exists(output));
        assertTrue(result.getCompressedSizeBytes() > 0);
        assertTrue(result.getCompressedSizeBytes() < originalContent.length, "Compressed size should be smaller than original");
        assertNull(result.getErrorMessage());
    }

    @Test
    void testSimulationCompressionHighPreset() throws IOException {
        Path input = tempDir.resolve("sample.mp4");
        byte[] originalContent = new byte[10000];
        Files.write(input, originalContent);

        Path output = tempDir.resolve("output_high.mp4");
        CompressionResult result = compressor.compress(input, output, "HIGH");

        assertTrue(result.isSuccess());
        assertTrue(Files.exists(output));
        // HIGH preset should compress more (approx 40% of original, so ~4000)
        assertTrue(result.getCompressedSizeBytes() <= 5000);
    }
}
