# User Guide

Complete guide for using the MODBUS TCP Service effectively.

## 📋 Table of Contents

### Core Features
- **[Device Management](device-management.md)** - Add, configure, and manage MODBUS devices
- **[Data Collection](data-collection.md)** - Collect and store sensor readings
- **[Monitoring & Health Checks](monitoring.md)** - Monitor device health and system status
- **[Configuration Management](configuration.md)** - Manage device configurations and settings

### Interfaces
- **[CLI Usage](cli-usage.md)** - Command-line interface guide
- **[Web API Usage](web-api-usage.md)** - REST API and Swagger UI guide

### Maintenance
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[Performance Tuning](performance.md)** - Optimize for your environment
- **[Backup & Recovery](backup-recovery.md)** - Data protection strategies

## 🎯 Quick Reference

### Common Tasks

| Task | CLI Command | API Endpoint |
|------|-------------|--------------|
| Add device | `python modbustcp.py device add --name "Meter" --type SDM120 --host 10.1.2.1 --unit 1` | `POST /api/v1/devices` |
| List devices | `python modbustcp.py device list` | `GET /api/v1/devices` |
| Test connection | `python modbustcp.py test-connection --host 10.1.2.1 --unit 1` | `POST /api/v1/devices/test-connection` |
| Collect data | `python modbustcp.py data collect <device-id>` | `POST /api/v1/readings/collect` |
| View latest readings | `python modbustcp.py data latest <device-id>` | `GET /api/v1/readings/latest/{device_id}` |
| Check health | `python modbustcp.py monitor health <device-id>` | `GET /api/v1/monitoring/health/{device_id}` |

### Device Types

| Type | Description | Registers | Typical Values |
|------|-------------|-----------|----------------|
| **SDM120** | Energy Meter | Voltage, Current, Power, Energy, Frequency | 230V, 12.5A, 2.8kW, 1250kWh, 50Hz |
| **PM2510-0D** | Dust Sensor | PM2.5, PM10 | 35µg/m³, 55µg/m³ |
| **XY-MD02** | Environmental | Temperature, Humidity | 23.5°C, 65.2%RH |
| **GENERIC** | Custom Device | Configurable | Varies |

## 📊 Understanding the System

### Data Flow

```
MODBUS Device → MODBUS TCP Service → Database → API/CLI → User
```

1. **Device Communication**: Service connects to MODBUS devices via TCP/IP
2. **Data Collection**: Reads configured registers from devices
3. **Data Storage**: Stores readings in PostgreSQL or InfluxDB
4. **Data Access**: Provides access via CLI commands or REST API
5. **Monitoring**: Tracks device health and system status

### Service Components

- **Core Service**: Main application logic
- **Database**: PostgreSQL (relational) + InfluxDB (time-series)
- **API Server**: REST API with Swagger documentation
- **CLI Interface**: Command-line tools
- **Monitoring**: Health checks and system status

## 🔧 System Architecture

The service follows clean architecture principles:

### Domain Layer
- **Entities**: Device, Reading, DeviceConfig
- **Value Objects**: DeviceId, DeviceType, ModbusAddress
- **Repository Interfaces**: Abstract data access contracts

### Application Layer
- **Use Cases**: DeviceManagement, DataCollection, Monitoring
- **Services**: Business logic and coordination

### Infrastructure Layer
- **MODBUS Client**: PyModbus TCP implementation
- **Database**: PostgreSQL and InfluxDB repositories
- **Configuration**: YAML-based settings

### Presentation Layer
- **CLI**: Command-line interface
- **API**: REST API with FastAPI and Swagger

## 📈 Data Management

### Data Types

**Device Data (PostgreSQL)**
- Device information and metadata
- Configuration settings
- Connection parameters

**Reading Data (PostgreSQL or InfluxDB)**
- Sensor measurements
- Timestamps
- Quality indicators

### Data Retention

Configure data retention policies:

```yaml
# config/config.yaml
monitoring:
  max_reading_age_hours: 24  # Keep readings for 24 hours
```

For InfluxDB, configure bucket retention:
```bash
influx bucket update --name readings --retention 30d
```

## 🔍 Monitoring & Alerts

### Health Check Types

1. **Connection Health**: Can the service reach the device?
2. **Data Freshness**: Are we receiving recent data?
3. **Service Health**: Is the service running properly?
4. **Database Health**: Are databases accessible?

### Status Indicators

| Status | Meaning | CLI Output | API Response |
|--------|---------|------------|--------------|
| 🟢 Healthy | Everything normal | `✅ Device healthy` | `"status": "healthy"` |
| 🟡 Warning | Minor issues | `⚠️ Device warning` | `"status": "warning"` |
| 🔴 Error | Serious problems | `❌ Device error` | `"status": "error"` |
| ⚫ Disconnected | No connection | `❌ Device disconnected` | `"status": "disconnected"` |

## 🛡️ Security Considerations

### Network Security
- Use firewall rules to restrict MODBUS TCP access
- Consider VPN for remote device access
- Monitor network traffic for anomalies

### Application Security
- Use environment variables for sensitive configuration
- Enable API authentication (when implemented)
- Regular security updates

### Data Security
- Database encryption at rest
- Secure backup strategies
- Access logging and monitoring

## 🚀 Performance Optimization

### Device Communication
- Adjust timeout values for network conditions
- Use appropriate polling intervals
- Batch register reads when possible

### Database Performance
- Monitor database connections
- Configure appropriate connection pools
- Regular database maintenance

### System Resources
- Monitor CPU and memory usage
- Scale horizontally with multiple instances
- Use caching for frequently accessed data

## 🤝 Integration

### External Systems

The service can integrate with:
- **SCADA systems** via REST API
- **IoT platforms** using data export
- **Monitoring tools** using health endpoints
- **Databases** for long-term storage
- **Visualization tools** like Grafana

### Data Export

Export data in various formats:
```bash
# JSON export
curl "http://localhost:8000/api/v1/readings?device_id=123&format=json"

# CSV export (when implemented)
python modbustcp.py data export --device-id 123 --format csv --output data.csv
```

## 📖 Best Practices

### Device Management
1. Use descriptive device names
2. Document device locations and purposes
3. Regular connectivity testing
4. Monitor device health continuously

### Data Collection
1. Set appropriate polling intervals
2. Handle connection failures gracefully
3. Validate data quality
4. Archive old data appropriately

### System Maintenance
1. Regular backup of configuration and data
2. Monitor log files for errors
3. Update dependencies regularly
4. Test disaster recovery procedures

## 🆘 Getting Help

If you need assistance:

1. **Check the [Troubleshooting Guide](troubleshooting.md)** first
2. **Review relevant sections** in this user guide
3. **Check the [API Reference](../api-reference/)** for API questions
4. **Search [GitHub Issues](https://github.com/devonixcompany/MODBUSTCP/issues)** for similar problems
5. **Open a new issue** if you can't find a solution

## 📚 Further Reading

- **[Developer Guide](../developer-guide/)** - Technical implementation details
- **[API Reference](../api-reference/)** - Complete API documentation
- **[Deployment Guide](../deployment/)** - Production deployment
- **[Examples](../examples/)** - Practical examples and tutorials