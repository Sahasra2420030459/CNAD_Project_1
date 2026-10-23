package com.videoplatform.controller;

import com.videoplatform.queue.MessageQueueService;
import com.videoplatform.storage.StorageService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/health")
@Tag(name = "Health & Readiness", description = "Endpoints for platform diagnostics, queue depth, and adapter status")
public class HealthController {

    private final StorageService storageService;
    private final MessageQueueService messageQueueService;

    public HealthController(StorageService storageService, MessageQueueService messageQueueService) {
        this.storageService = storageService;
        this.messageQueueService = messageQueueService;
    }

    @GetMapping
    @Operation(summary = "Check service health", description = "Probes active storage and queue adapter states and current queue depth.")
    @ApiResponse(responseCode = "200", description = "Service is operational")
    public ResponseEntity<Map<String, Object>> checkHealth() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "UP");
        health.put("timestamp", Instant.now().toString());
        health.put("storageAdapter", storageService.getStorageType());
        health.put("queueAdapter", messageQueueService.getQueueType());
        health.put("queueDepth", messageQueueService.getQueueDepth());
        return ResponseEntity.ok(health);
    }
}
