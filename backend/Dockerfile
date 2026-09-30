# ==========================================
# Stage 1 — Build JAR
# ==========================================
FROM maven:3.9.9-amazoncorretto-11 AS builder

WORKDIR /app

# Copy Maven configuration first
COPY pom.xml .

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build application
RUN mvn clean package \
    -Dspring.profiles.active=build \
    -DskipTests


# ==========================================
# Stage 2 — Run JAR
# ==========================================
FROM amazoncorretto:11-alpine-jdk

WORKDIR /app

# Copy generated JAR
COPY --from=builder /app/target/*.jar app.jar

# Application port
ENV SERVER_PORT=8084

EXPOSE 8084

# Start Spring Boot application
CMD ["java", "-jar", "app.jar"]