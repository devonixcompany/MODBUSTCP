# Multi-stage Docker build for MODBUS TCP Service
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
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
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/modbustcp/.local

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY setup.py ./
COPY requirements.txt ./

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

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.insert(0, '/app/src'); from infrastructure.modbus import PyModbusClient; print('OK')" || exit 1

# Default command
CMD ["python", "-m", "presentation.cli.main", "--help"]

# Expose default MODBUS port for documentation
EXPOSE 502

# Labels
LABEL maintainer="DevonixCompany <dev@devonixcompany.com>"
LABEL version="1.0.0"
LABEL description="Production-ready MODBUS TCP service with clean architecture"