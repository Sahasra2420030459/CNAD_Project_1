# Stage 1: Build Java Worker
FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /app

COPY pom.xml .
RUN mvn dependency:go-offline -B || true

COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Runtime with OpenJDK 21 + FFmpeg
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app

# Install FFmpeg and required codecs
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Verify FFmpeg installation
RUN ffmpeg -version

# Setup non-root user
RUN useradd -m -u 1000 workeruser && \
    mkdir -p /app/uploads/originals /app/uploads/compressed && \
    chown -R workeruser:workeruser /app

COPY --from=build /app/target/*.jar worker.jar

USER workeruser

ENV SPRING_PROFILES_ACTIVE=local
ENV FFMPEG_PATH=ffmpeg
ENV WORKER_FFMPEG_SIMULATION_MODE=false

ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-jar", "worker.jar"]
