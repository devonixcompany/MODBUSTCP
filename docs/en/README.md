# MODBUS TCP Service - English Documentation

Welcome to the comprehensive documentation for the MODBUS TCP Service. This service provides a production-ready solution for collecting data from MODBUS devices with clean architecture principles.

## 📋 Table of Contents

### 🚀 [Getting Started](getting-started/)
New to the MODBUS TCP Service? Start here!
- [Quick Start Guide](getting-started/quick-start.md)
- [Installation Guide](getting-started/installation.md)
- [First Steps](getting-started/first-steps.md)
- [Basic Configuration](getting-started/configuration.md)

### 👥 [User Guide](user-guide/)
Complete guide for end users
- [Device Management](user-guide/device-management.md)
- [Data Collection](user-guide/data-collection.md)
- [Monitoring & Health Checks](user-guide/monitoring.md)
- [Configuration Management](user-guide/configuration.md)
- [CLI Usage](user-guide/cli-usage.md)
- [Troubleshooting](user-guide/troubleshooting.md)

### 🛠️ [Developer Guide](developer-guide/)
Technical documentation for developers
- [Architecture Overview](developer-guide/architecture.md)
- [Clean Architecture Principles](developer-guide/clean-architecture.md)
- [Domain Layer](developer-guide/domain-layer.md)
- [Application Layer](developer-guide/application-layer.md)
- [Infrastructure Layer](developer-guide/infrastructure-layer.md)
- [Presentation Layer](developer-guide/presentation-layer.md)
- [Adding New Devices](developer-guide/adding-devices.md)
- [Database Schema](developer-guide/database-schema.md)
- [Testing Guide](developer-guide/testing.md)
- [Contributing](developer-guide/contributing.md)

### 🌐 [API Reference](api-reference/)
Complete REST API documentation
- [API Overview](api-reference/overview.md)
- [Authentication](api-reference/authentication.md)
- [Device Endpoints](api-reference/devices.md)
- [Reading Endpoints](api-reference/readings.md)
- [Monitoring Endpoints](api-reference/monitoring.md)
- [Error Handling](api-reference/errors.md)
- [OpenAPI Specification](api-reference/openapi.md)

### 🚀 [Deployment](deployment/)
Production deployment guides
- [Docker Deployment](deployment/docker.md)
- [Kubernetes Deployment](deployment/kubernetes.md)
- [Environment Configuration](deployment/environment.md)
- [Database Setup](deployment/database.md)
- [Monitoring & Logging](deployment/monitoring.md)
- [Security Considerations](deployment/security.md)
- [Performance Tuning](deployment/performance.md)

### 💡 [Examples](examples/)
Practical examples and tutorials
- [Basic Usage Examples](examples/basic-usage.md)
- [Device Configuration Examples](examples/device-configs.md)
- [API Usage Examples](examples/api-examples.md)
- [Integration Examples](examples/integrations.md)
- [Custom Device Implementation](examples/custom-devices.md)

## 🎯 Quick Links

| Task | Documentation |
|------|---------------|
| Install and run the service | [Quick Start Guide](getting-started/quick-start.md) |
| Add a new MODBUS device | [Device Management](user-guide/device-management.md) |
| Use the REST API | [API Overview](api-reference/overview.md) |
| Deploy to production | [Docker Deployment](deployment/docker.md) |
| Extend the codebase | [Architecture Overview](developer-guide/architecture.md) |
| Troubleshoot issues | [Troubleshooting](user-guide/troubleshooting.md) |

## 📖 About This Service

The MODBUS TCP Service is a production-ready solution that transforms legacy individual scripts into a unified, maintainable system. It provides:

- **Clean Architecture** - Maintainable and testable codebase
- **Multi-Interface** - Both CLI and REST API interfaces
- **Database Persistence** - PostgreSQL and InfluxDB support
- **Docker Support** - Production-ready containerization
- **Comprehensive Monitoring** - Health checks and system status
- **Multi-Device Support** - SDM120, PM2510-0D, XY-MD02, and generic devices

## 🔧 Key Features

### Supported Devices
- **SDM120** - Energy meters with voltage, current, power measurements
- **PM2510-0D** - Dust sensors with PM2.5 and PM10 monitoring
- **XY-MD02** - Environmental sensors with temperature and humidity
- **Generic MODBUS** - Configurable support for any MODBUS device

### Interfaces
- **Command Line Interface (CLI)** - Full-featured terminal interface
- **REST API** - Web-friendly API with Swagger documentation
- **Configuration Files** - YAML-based device configuration

### Data Storage
- **PostgreSQL** - Relational data for devices and configurations
- **InfluxDB** - Time-series data for sensor readings
- **In-Memory** - Development and testing support

## 🤝 Getting Help

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/devonixcompany/MODBUSTCP/issues)
- **Discussions**: Join the community discussions
- **Documentation**: This comprehensive guide covers all aspects of the service

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.