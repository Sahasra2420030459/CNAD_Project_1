package com.videoplatform.repository;

import com.videoplatform.entity.JobStatus;
import com.videoplatform.entity.ProcessingJob;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ProcessingJobRepository extends JpaRepository<ProcessingJob, Long> {
    Page<ProcessingJob> findByUserId(Long userId, Pageable pageable);
    Page<ProcessingJob> findByUserIdAndStatus(Long userId, JobStatus status, Pageable pageable);
    Optional<ProcessingJob> findByIdAndUserId(Long id, Long userId);
    long countByUserId(Long userId);
    long countByUserIdAndStatus(Long userId, JobStatus status);
}
