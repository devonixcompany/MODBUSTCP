# Getting Started

Welcome to the MODBUS TCP Service! This section will help you get up and running quickly.

## 📋 Prerequisites

Before you begin, make sure you have:

- **Python 3.11+** (for development installation)
- **Docker & Docker Compose** (for production deployment)
- **Access to MODBUS devices** on your network
- **Basic knowledge** of MODBUS protocol (helpful but not required)

## 🚀 Choose Your Path

### Option 1: Quick Start with Docker (Recommended)
Perfect for production use or if you want to get started immediately.

👉 **[Quick Start Guide](quick-start.md)**

### Option 2: Development Installation
Ideal for developers who want to modify or extend the service.

👉 **[Installation Guide](installation.md)**

## 📚 What's Next?

After completing the installation:

1. **[First Steps](first-steps.md)** - Learn the basic operations
2. **[Basic Configuration](configuration.md)** - Set up your devices
3. **[User Guide](../user-guide/)** - Dive deeper into features

## 🎯 Quick Overview

The MODBUS TCP Service provides two main interfaces:

### Command Line Interface (CLI)
```bash
# Add a device
python modbustcp.py device add --name "Energy Meter" --type SDM120 --host 10.1.2.1 --unit 1

# Collect data
python modbustcp.py data collect <device-id>

# Monitor health
python modbustcp.py monitor health-all
```

### REST API Interface
```bash
# Start API server
python api_server.py

# Access Swagger UI
open http://localhost:8000/docs
```

## 🔧 Supported Devices

The service comes with built-in support for:

| Device | Type | Measurements |
|--------|------|-------------|
| **SDM120** | Energy Meter | Voltage, Current, Power, Energy, Frequency |
| **PM2510-0D** | Dust Sensor | PM2.5, PM10 Air Quality |
| **XY-MD02** | Environmental | Temperature, Humidity |
| **Generic** | Any MODBUS | Configurable Registers |

## 💾 Data Storage Options

Choose your preferred data storage:

- **PostgreSQL** - For relational data (devices, configurations)
- **InfluxDB** - For time-series data (sensor readings)
- **In-Memory** - For development and testing

## 🐳 Deployment Options

### Development
- Local Python installation
- In-memory data storage
- CLI interface

### Production
- Docker containers
- PostgreSQL + InfluxDB
- REST API + CLI
- Health monitoring
- Horizontal scaling

## 🤔 Need Help?

If you run into issues:

1. Check the **[Troubleshooting Guide](../user-guide/troubleshooting.md)**
2. Review the **[FAQ section](../user-guide/troubleshooting.md#faq)**
3. Open an issue on GitHub

Let's get started! 🚀