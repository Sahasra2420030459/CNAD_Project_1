package com.videoplatform.repository;

import com.videoplatform.entity.JobStatus;
import com.videoplatform.entity.VideoJob;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface VideoJobRepository extends JpaRepository<VideoJob, Long> {

    Page<VideoJob> findByUserId(Long userId, Pageable pageable);

    Page<VideoJob> findByUserIdAndStatus(Long userId, JobStatus status, Pageable pageable);

    Optional<VideoJob> findByIdAndUserId(Long id, Long userId);

    List<VideoJob> findByStatusOrderByCreatedAtAsc(JobStatus status);

    long countByUserId(Long userId);

    long countByUserIdAndStatus(Long userId, JobStatus status);

    @Query("SELECT COALESCE(SUM(v.originalSizeBytes), 0) FROM VideoJob v WHERE v.user.id = :userId")
    Long sumOriginalSizeBytesByUserId(@Param("userId") Long userId);

    @Query("SELECT COALESCE(SUM(v.compressedSizeBytes), 0) FROM VideoJob v WHERE v.user.id = :userId AND v.status = 'COMPLETED'")
    Long sumCompressedSizeBytesByUserId(@Param("userId") Long userId);
}
