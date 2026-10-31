package com.videoplatform.config;

import com.videoplatform.entity.Role;
import com.videoplatform.repository.RoleRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

/**
 * Initializes default application roles upon startup if they do not exist.
 * Ensures compatibility across all database backends (H2, MySQL, PostgreSQL).
 */
@Component
public class DataInitializer implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(DataInitializer.class);

    private final RoleRepository roleRepository;

    public DataInitializer(RoleRepository roleRepository) {
        this.roleRepository = roleRepository;
    }

    @Override
    public void run(String... args) {
        try {
            if (roleRepository.findByName("ROLE_USER").isEmpty()) {
                roleRepository.save(new Role("ROLE_USER"));
                log.info("Initialized default role: ROLE_USER");
            }
            if (roleRepository.findByName("ROLE_ADMIN").isEmpty()) {
                roleRepository.save(new Role("ROLE_ADMIN"));
                log.info("Initialized default role: ROLE_ADMIN");
            }
        } catch (Exception e) {
            log.warn("Could not pre-seed roles on startup: {}", e.getMessage());
        }
    }
}
