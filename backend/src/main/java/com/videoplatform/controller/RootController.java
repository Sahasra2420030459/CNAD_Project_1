package com.videoplatform.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * Root Controller for cloud platform health probes (e.g. Render, Railway, AWS ALB).
 */
@RestController
@Tag(name = "Root Probe", description = "Root health endpoint for cloud load balancers and platform monitors")
public class RootController {

    @GetMapping("/")
    @Operation(summary = "Root health probe", description = "Returns 200 OK to satisfy cloud hosting platform root health checks.")
    public ResponseEntity<Map<String, String>> rootProbe() {
        return ResponseEntity.ok(Map.of(
                "status", "UP",
                "service", "Video Platform REST API",
                "docs", "/swagger-ui/index.html",
                "health", "/api/health"
        ));
    }
}
