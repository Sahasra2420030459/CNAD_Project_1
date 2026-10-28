package com.videoplatform.config;

import org.hibernate.exception.JDBCConnectionException;
import org.springframework.boot.diagnostics.AbstractFailureAnalyzer;
import org.springframework.boot.diagnostics.FailureAnalysis;

/**
 * Custom FailureAnalyzer that catches JDBC connection failures and prints an
 * actionable, beginner-friendly diagnostic guide with exact configuration steps.
 */
public class DatabaseConnectionFailureAnalyzer extends AbstractFailureAnalyzer<JDBCConnectionException> {

    @Override
    protected FailureAnalysis analyze(Throwable rootFailure, JDBCConnectionException cause) {
        String rootMsg = cause.getCause() != null ? cause.getCause().getMessage() : cause.getMessage();
        String description = "Cannot establish JDBC Connection to database.\n" +
                "Details: " + rootMsg;

        String action = "\n" +
                "========================================================================================\n" +
                "DATABASE CONNECTION FAILED - QUICK RESOLUTION GUIDE\n" +
                "========================================================================================\n" +
                "1. RUNNING LOCALLY WITHOUT MYSQL INSTALLED (Recommended for laptop testing):\n" +
                "   Start the application with the built-in zero-install H2 profile:\n" +
                "   -> Set environment variable: SPRING_PROFILES_ACTIVE=h2\n" +
                "   -> Command: java -jar app.jar --spring.profiles.active=h2\n" +
                "   (This creates a local persistent database in ./data/videoplatform automatically)\n\n" +
                "2. CONNECTING TO CLOUD MYSQL (Render / Railway / Aiven / TiDB / Azure):\n" +
                "   Set these environment variables in your deployment dashboard:\n" +
                "   -> DB_HOST     : your remote database host (e.g. mysql-xxx.aivencloud.com)\n" +
                "   -> DB_PORT     : 3306 (or provider port)\n" +
                "   -> DB_NAME     : videoplatform\n" +
                "   -> DB_USERNAME : your database username\n" +
                "   -> DB_PASSWORD : your database password\n" +
                "   -> DB_USE_SSL  : true\n" +
                "   -> SPRING_PROFILES_ACTIVE : prod\n\n" +
                "3. CHECK NETWORK ACCESS & FIREWALL:\n" +
                "   -> Ensure your cloud database provider allows connections from your hosting IP\n" +
                "      (in Aiven/TiDB/Azure, allow 0.0.0.0/0 for public internet access).\n" +
                "========================================================================================";

        return new FailureAnalysis(description, action, cause);
    }
}
