# Installation Guide

This guide covers different installation methods for the MODBUS TCP Service.

## 🎯 Choose Your Installation Method

### 🐳 Docker Installation (Recommended)

Best for production use and quick setup.

**Prerequisites:**
- Docker Engine 20.10+
- Docker Compose 2.0+

**Installation:**

```bash
# Clone the repository
git clone https://github.com/devonixcompany/MODBUSTCP.git
cd MODBUSTCP

# Start all services
docker-compose up -d

# Verify installation
docker-compose ps
curl http://localhost:8000/api/v1/health
```

### 🐍 Python Installation

Best for development and customization.

**Prerequisites:**
- Python 3.11 or higher
- pip package manager

**Installation:**

```bash
# Clone the repository
git clone https://github.com/devonixcompany/MODBUSTCP.git
cd MODBUSTCP

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Verify installation
python modbustcp.py --help
```

### 📦 Package Installation

Install from PyPI (when available).

```bash
# Install from PyPI
pip install modbustcp-service

# Verify installation
modbustcp --help
```

## 🔧 Database Setup

### Option 1: Docker Databases (Included)

When using `docker-compose up -d`, databases are automatically configured:

- **PostgreSQL**: `localhost:5432`
- **InfluxDB**: `localhost:8086`

### Option 2: External Databases

If you have existing databases:

**PostgreSQL Setup:**
```sql
-- Create database and user
CREATE DATABASE modbustcp_db;
CREATE USER modbustcp_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE modbustcp_db TO modbustcp_user;
```

**InfluxDB Setup:**
```bash
# Create bucket
influx bucket create -n readings -o modbustcp

# Create token
influx auth create --org modbustcp --all-access
```

**Environment Configuration:**
```bash
export DATABASE_URL="******localhost:5432/modbustcp_db"
export INFLUXDB_URL="http://localhost:8086"
export INFLUXDB_TOKEN="your-token"
export INFLUXDB_ORG="modbustcp"
export INFLUXDB_BUCKET="readings"
```

### Option 3: In-Memory (Development)

For development without external databases:

```bash
# Use in-memory storage
export READING_STORE="memory"
```

## 🔐 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Copy example configuration
cp .env.example .env

# Edit configuration
nano .env
```

Key settings:
```bash
# Application
MODBUS_ENVIRONMENT=production
MODBUS_DEBUG=false

# Database
DATABASE_URL=******localhost:5432/modbustcp_db
READING_STORE=postgresql  # or influxdb

# API
API_HOST=0.0.0.0
API_PORT=8000
```

### Configuration File

Edit `config/config.yaml`:

```yaml
# Basic settings
debug: false
environment: "production"

# Database configuration
database:
  connection_string: "******localhost:5432/modbustcp_db"
  reading_store: "postgresql"

# API configuration
api:
  host: "0.0.0.0"
  port: 8000
```

## 🧪 Verify Installation

### Test CLI Interface

```bash
# Check version
python modbustcp.py --version

# Test connection
python modbustcp.py test-connection --host 127.0.0.1 --unit 1

# List available commands
python modbustcp.py --help
```

### Test API Interface

```bash
# Start API server
python api_server.py

# In another terminal, test endpoints
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/docs  # Swagger UI
```

### Test Database Connection

```bash
# Test PostgreSQL connection
python -c "
import asyncio
from src.infrastructure.database.postgresql.repositories import PostgreSQLDeviceRepository
repo = PostgreSQLDeviceRepository('******localhost:5432/modbustcp_db')
print('PostgreSQL connection: OK')
"

# Test InfluxDB connection (if configured)
python -c "
from src.infrastructure.database.influxdb.repositories import InfluxDBReadingRepository
repo = InfluxDBReadingRepository('http://localhost:8086', 'token', 'org', 'bucket')
print('InfluxDB connection: OK')
"
```

## 📋 System Requirements

### Minimum Requirements

- **CPU**: 1 core, 2 GHz
- **RAM**: 512 MB
- **Storage**: 1 GB available space
- **Network**: Access to MODBUS devices on TCP/IP network

### Recommended Requirements

- **CPU**: 2+ cores, 2.5+ GHz
- **RAM**: 2+ GB
- **Storage**: 10+ GB available space (for data retention)
- **Network**: Gigabit network interface

### Operating System Support

**Docker Installation:**
- Linux (any Docker-supported distribution)
- macOS 10.15+
- Windows 10/11 with WSL2

**Python Installation:**
- Ubuntu 20.04+ / Debian 11+
- CentOS 8+ / RHEL 8+
- macOS 10.15+
- Windows 10/11

## 🔧 Development Setup

For developers who want to contribute:

```bash
# Clone and setup
git clone https://github.com/devonixcompany/MODBUSTCP.git
cd MODBUSTCP

# Create development environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Install development tools
pip install pytest pytest-asyncio black flake8 mypy

# Run tests
pytest

# Run linting
black src/
flake8 src/
mypy src/
```

## 🚀 Production Deployment

For production deployments, see:
- **[Docker Deployment Guide](../deployment/docker.md)**
- **[Environment Configuration](../deployment/environment.md)**
- **[Security Considerations](../deployment/security.md)**

## 🔍 Troubleshooting

### Common Installation Issues

**Python version error:**
```bash
# Check Python version
python --version  # Should be 3.11+

# Use specific Python version
python3.11 -m venv venv
```

**Docker permission error:**
```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker
```

**Port already in use:**
```bash
# Find process using port
sudo lsof -i :8000

# Change port in configuration
export API_PORT=8080
```

**Database connection error:**
```bash
# Check database status
docker-compose logs postgres
docker-compose logs influxdb

# Reset databases
docker-compose down -v
docker-compose up -d
```

For more troubleshooting help, see the **[Troubleshooting Guide](../user-guide/troubleshooting.md)**.

## ✅ Next Steps

After successful installation:

1. **[First Steps](first-steps.md)** - Learn basic operations
2. **[Configuration](configuration.md)** - Set up your devices
3. **[User Guide](../user-guide/)** - Explore all features

Need help? Check the **[Getting Help](../README.md#getting-help)** section.