# Stage 1: Build Java Spring Boot Application
FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /app

# Cache dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B || true

# Copy source code and package
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Minimal Runtime Environment
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app

# Create non-root user and shared uploads folder
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/uploads/originals /app/uploads/compressed && \
    chown -R appuser:appuser /app

COPY --from=build /app/target/*.jar app.jar

USER appuser
EXPOSE 8080

ENV SPRING_PROFILES_ACTIVE=local
ENV PORT_BACKEND=8080

ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]
