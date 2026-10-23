package com.videoplatform.repository;

import com.videoplatform.entity.Video;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface VideoRepository extends JpaRepository<Video, Long> {
    List<Video> findByUserId(Long userId);
    Optional<Video> findByIdAndUserId(Long id, Long userId);
}
