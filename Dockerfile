# =========================
# Builder stage
# =========================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# =========================
# Runtime stage
# =========================
FROM python:3.11-slim

# Set timezone to UTC
ENV TZ=UTC

# Install cron and runtime dependencies
RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Create volume mount points
RUN mkdir -p /data /cron

# Copy application code and keys
COPY app/ app/
COPY student_public.pem .
COPY instructor_public.pem .
COPY instructor_private.pem .

# Copy initial persistent files (will be overridden by volumes)
COPY data/encrypted_seed.txt /data/encrypted_seed.txt
COPY data/encrypted_seed.sig /data/encrypted_seed.sig
COPY data/cron/last_code.txt /cron/last_code.txt

# Copy cron job file
COPY 2fa-cron /etc/cron.d/2fa-cron
# Set permissions
RUN chmod 0644 /etc/cron.d/2fa-cron && \
    crontab /etc/cron.d/2fa-cron && \
    chmod -R 777 /data /cron

# Expose API port
EXPOSE 8080

# Start cron and API server together
CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 8080
