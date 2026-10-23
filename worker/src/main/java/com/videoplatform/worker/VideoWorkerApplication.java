package com.videoplatform.worker;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class VideoWorkerApplication {

    public static void main(String[] args) {
        SpringApplication.run(VideoWorkerApplication.class, args);
    }
}
