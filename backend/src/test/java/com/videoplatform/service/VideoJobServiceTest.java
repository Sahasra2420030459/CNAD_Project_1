package com.videoplatform.service;

import com.videoplatform.dto.BatchUploadResponse;
import com.videoplatform.dto.JobStatusResponse;
import com.videoplatform.dto.VideoJobResponse;
import com.videoplatform.entity.JobStatus;
import com.videoplatform.entity.User;
import com.videoplatform.entity.VideoJob;
import com.videoplatform.exception.InvalidFileException;
import com.videoplatform.exception.UnauthorizedAccessException;
import com.videoplatform.queue.JobQueueMessage;
import com.videoplatform.queue.MessageQueueService;
import com.videoplatform.repository.UserRepository;
import com.videoplatform.repository.VideoJobRepository;
import com.videoplatform.storage.StorageService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.mock.web.MockMultipartFile;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class VideoJobServiceTest {

    @Mock
    private VideoJobRepository videoJobRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private StorageService storageService;

    @Mock
    private MessageQueueService messageQueueService;

    private VideoJobService videoJobService;
    private User testUser;

    @BeforeEach
    void setUp() {
        videoJobService = new VideoJobService(videoJobRepository, userRepository, storageService, messageQueueService);
        testUser = new User("student@college.edu", "hashed_pw", "Student Name");
        testUser.setId(1L);
    }

    @Test
    void testCreateJobSuccess() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "lecture.mp4",
                "video/mp4",
                new byte[1024]
        );

        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
        when(storageService.store(any(), eq("originals"))).thenReturn("originals/uuid-lecture.mp4");

        VideoJob savedJob = new VideoJob();
        savedJob.setId(10L);
        savedJob.setUser(testUser);
        savedJob.setOriginalFileName("lecture.mp4");
        savedJob.setOriginalStoragePath("originals/uuid-lecture.mp4");
        savedJob.setOriginalSizeBytes(1024L);
        savedJob.setStatus(JobStatus.QUEUED);
        savedJob.setProgress(0);
        savedJob.setRetryCount(0);
        savedJob.setPreset("HIGH");
        savedJob.setTargetResolution("854x480");

        when(videoJobRepository.save(any(VideoJob.class))).thenReturn(savedJob);

        VideoJobResponse response = videoJobService.createJob(file, "HIGH", 1L);

        assertNotNull(response);
        assertEquals(10L, response.getId());
        assertEquals("lecture.mp4", response.getOriginalFileName());
        assertEquals(JobStatus.QUEUED, response.getStatus());
        assertEquals("HIGH", response.getPreset());
        assertEquals("854x480", response.getTargetResolution());

        ArgumentCaptor<JobQueueMessage> msgCaptor = ArgumentCaptor.forClass(JobQueueMessage.class);
        verify(messageQueueService, times(1)).enqueueJob(msgCaptor.capture());
        JobQueueMessage enqueued = msgCaptor.getValue();
        assertEquals(10L, enqueued.getJobId());
        assertEquals(1L, enqueued.getUserId());
        assertEquals("HIGH", enqueued.getPreset());
    }

    @Test
    void testCreateBatchJobsSuccess() {
        MockMultipartFile file1 = new MockMultipartFile("files", "clip1.mp4", "video/mp4", new byte[512]);
        MockMultipartFile file2 = new MockMultipartFile("files", "clip2.mp4", "video/mp4", new byte[512]);

        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
        when(storageService.store(any(), eq("originals"))).thenReturn("originals/test.mp4");

        VideoJob savedJob = new VideoJob();
        savedJob.setId(101L);
        savedJob.setUser(testUser);
        savedJob.setOriginalFileName("clip.mp4");
        savedJob.setOriginalStoragePath("originals/test.mp4");
        savedJob.setOriginalSizeBytes(512L);
        savedJob.setStatus(JobStatus.QUEUED);

        when(videoJobRepository.save(any(VideoJob.class))).thenReturn(savedJob);

        BatchUploadResponse batchResponse = videoJobService.createBatchJobs(List.of(file1, file2), "MEDIUM", 1L);

        assertNotNull(batchResponse);
        assertEquals(2, batchResponse.getTotalUploaded());
        assertEquals(2, batchResponse.getSuccessfulJobs().size());
        assertTrue(batchResponse.getFailedFiles().isEmpty());
    }

    @Test
    void testRetryFailedJobSuccess() {
        VideoJob failedJob = new VideoJob();
        failedJob.setId(50L);
        failedJob.setUser(testUser);
        failedJob.setStatus(JobStatus.FAILED);
        failedJob.setOriginalFileName("corrupted.mp4");
        failedJob.setOriginalStoragePath("originals/corrupted.mp4");
        failedJob.setPreset("MEDIUM");
        failedJob.setErrorMessage("FFmpeg transcoding error");
        failedJob.setRetryCount(0);

        when(videoJobRepository.findById(50L)).thenReturn(Optional.of(failedJob));
        when(videoJobRepository.save(any(VideoJob.class))).thenAnswer(invocation -> invocation.getArgument(0));

        VideoJobResponse retryResponse = videoJobService.retryJob(50L, 1L);

        assertNotNull(retryResponse);
        assertEquals(JobStatus.QUEUED, retryResponse.getStatus());
        assertEquals(0, retryResponse.getProgress());
        assertEquals(1, retryResponse.getRetryCount());
        assertNull(retryResponse.getErrorMessage());

        verify(messageQueueService, times(1)).enqueueJob(any(JobQueueMessage.class));
    }

    @Test
    void testRetryNonFailedJobThrows() {
        VideoJob activeJob = new VideoJob();
        activeJob.setId(60L);
        activeJob.setUser(testUser);
        activeJob.setStatus(JobStatus.PROCESSING);

        when(videoJobRepository.findById(60L)).thenReturn(Optional.of(activeJob));

        InvalidFileException ex = assertThrows(InvalidFileException.class, () -> {
            videoJobService.retryJob(60L, 1L);
        });
        assertTrue(ex.getMessage().contains("Only FAILED jobs are eligible for retry"));
        verify(messageQueueService, never()).enqueueJob(any());
    }

    @Test
    void testRetryJobEnforcesOwnership() {
        User otherUser = new User("other@college.edu", "hash", "Other User");
        otherUser.setId(99L);

        VideoJob failedJob = new VideoJob();
        failedJob.setId(70L);
        failedJob.setUser(otherUser);
        failedJob.setStatus(JobStatus.FAILED);

        when(videoJobRepository.findById(70L)).thenReturn(Optional.of(failedJob));

        assertThrows(UnauthorizedAccessException.class, () -> {
            videoJobService.retryJob(70L, 1L);
        });
    }

    @Test
    void testGetJobStatusEnforcesOwnership() {
        User otherUser = new User("other@college.edu", "hash", "Other User");
        otherUser.setId(99L);

        VideoJob job = new VideoJob();
        job.setId(80L);
        job.setUser(otherUser);
        job.setStatus(JobStatus.QUEUED);

        when(videoJobRepository.findById(80L)).thenReturn(Optional.of(job));

        assertThrows(UnauthorizedAccessException.class, () -> {
            videoJobService.getJobStatus(80L, 1L);
        });
    }

    @Test
    void testGetJobStatusSuccess() {
        VideoJob job = new VideoJob();
        job.setId(90L);
        job.setUser(testUser);
        job.setStatus(JobStatus.PROCESSING);
        job.setProgress(45);
        job.setOriginalFileName("sample.mp4");
        job.setPreset("MEDIUM");

        when(videoJobRepository.findById(90L)).thenReturn(Optional.of(job));

        JobStatusResponse status = videoJobService.getJobStatus(90L, 1L);
        assertNotNull(status);
        assertEquals(90L, status.getId());
        assertEquals(JobStatus.PROCESSING, status.getStatus());
        assertEquals(45, status.getProgress());
    }

    @Test
    void testValidateFileRejectsInvalidExtension() {
        MockMultipartFile badFile = new MockMultipartFile(
                "file",
                "malicious.exe",
                "application/octet-stream",
                new byte[50]
        );

        assertThrows(InvalidFileException.class, () -> videoJobService.validateFile(badFile));
    }

    @Test
    void testValidateFileRejectsEmpty() {
        MockMultipartFile emptyFile = new MockMultipartFile(
                "file",
                "empty.mp4",
                "video/mp4",
                new byte[0]
        );

        assertThrows(InvalidFileException.class, () -> videoJobService.validateFile(emptyFile));
    }

    @Test
    void testLoadCompressedVideoEnforcesOwnership() {
        User otherUser = new User("other@college.edu", "pw", "Other User");
        otherUser.setId(99L);

        VideoJob job = new VideoJob();
        job.setId(20L);
        job.setUser(otherUser);
        job.setStatus(JobStatus.COMPLETED);
        job.setCompressedStoragePath("compressed/test.mp4");

        when(videoJobRepository.findById(20L)).thenReturn(Optional.of(job));

        assertThrows(UnauthorizedAccessException.class, () -> {
            videoJobService.loadCompressedVideo(20L, 1L);
        });
    }

    @Test
    void testLoadCompressedVideoThrowsWhenIncomplete() {
        VideoJob pendingJob = new VideoJob();
        pendingJob.setId(30L);
        pendingJob.setUser(testUser);
        pendingJob.setStatus(JobStatus.PROCESSING);

        when(videoJobRepository.findById(30L)).thenReturn(Optional.of(pendingJob));

        assertThrows(InvalidFileException.class, () -> {
            videoJobService.loadCompressedVideo(30L, 1L);
        });
    }

    @Test
    void testPresetNormalizationAndResolution() {
        assertEquals("MEDIUM", VideoJobService.normalizePreset(null));
        assertEquals("LOW", VideoJobService.normalizePreset("low"));
        assertEquals("HIGH", VideoJobService.normalizePreset("HIGH"));
        assertEquals("MEDIUM", VideoJobService.normalizePreset("unknown"));

        assertEquals("1920x1080", VideoJobService.determineResolution("LOW"));
        assertEquals("1280x720", VideoJobService.determineResolution("MEDIUM"));
        assertEquals("854x480", VideoJobService.determineResolution("HIGH"));
    }
}
