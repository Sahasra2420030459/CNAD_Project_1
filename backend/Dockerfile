FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /app

ENV MAVEN_OPTS="-Xmx384m -XX:+UseSerialGC"

COPY pom.xml ./pom.xml
COPY src ./src

RUN mvn clean package -DskipTests --batch-mode

FROM eclipse-temurin:21-jre-jammy
WORKDIR /app

RUN mkdir -p /app/data /app/uploads

COPY --from=build /app/target/*.jar app.jar

ENV SPRING_PROFILES_ACTIVE=h2
ENV PORT=8080

EXPOSE 8080

ENTRYPOINT ["java", "-Xmx384m", "-XX:+UseSerialGC", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]
