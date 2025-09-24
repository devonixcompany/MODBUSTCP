# Multi-stage Docker build for MODBUS TCP Service
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r modbustcp && useradd -r -g modbustcp modbustcp

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/modbustcp/.local

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY migrations/ ./migrations/
COPY setup.py ./
COPY requirements.txt ./
COPY alembic.ini ./
COPY modbustcp.py ./
COPY api_server.py ./

# Create necessary directories
RUN mkdir -p /var/log/modbustcp /app/data && \
    chown -R modbustcp:modbustcp /var/log/modbustcp /app/data /app

# Switch to non-root user
USER modbustcp

# Set Python path
ENV PATH="/home/modbustcp/.local/bin:$PATH"
ENV PYTHONPATH="/app/src:$PYTHONPATH"

# Install application
RUN pip install --user -e .

# Health check for API
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Default command (can be overridden)
CMD ["python", "api_server.py"]

# Expose API port
EXPOSE 8000

# Labels
LABEL maintainer="DevonixCompany <dev@devonixcompany.com>"
LABEL version="1.0.0"
LABEL description="Production-ready MODBUS TCP service with REST API and database persistence"