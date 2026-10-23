package com.videoplatform.worker.repository;

import com.videoplatform.worker.entity.JobStatus;
import com.videoplatform.worker.entity.VideoJob;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface VideoJobRepository extends JpaRepository<VideoJob, Long> {
    List<VideoJob> findByStatusOrderByCreatedAtAsc(JobStatus status);
}
