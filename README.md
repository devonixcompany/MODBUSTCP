# MODBUS TCP Service

A production-ready MODBUS TCP service built with clean architecture principles. This service provides a unified interface for reading data from various MODBUS devices including energy meters, environmental sensors, and air quality monitors.

## 🏗️ Architecture

This project follows Clean Architecture principles with clear separation of concerns:

```
src/
├── domain/                 # Business logic and entities
│   ├── entities/          # Core business entities
│   ├── value_objects/     # Immutable value objects
│   └── repositories/      # Repository interfaces
├── application/           # Use cases and application services
│   ├── use_cases/        # Business use cases
│   ├── services/         # Application services
│   └── interfaces/       # Infrastructure interfaces
├── infrastructure/       # External concerns
│   ├── modbus/           # MODBUS client implementation
│   ├── database/         # Data persistence
│   └── config/           # Configuration management
└── presentation/         # User interfaces
    ├── cli/              # Command-line interface
    └── api/              # REST API (future)
```

## 🚀 Features

- **Clean Architecture**: Maintainable, testable, and scalable codebase
- **Multi-Device Support**: SDM120, PM2510-0D, XY-MD02, and generic MODBUS devices
- **Production Ready**: Docker support, logging, error handling, monitoring
- **CLI Interface**: Comprehensive command-line tools for device management
- **Configuration Management**: YAML-based device configurations
- **Data Collection**: Automated polling and data storage
- **Health Monitoring**: Device health checks and status monitoring
- **Async Support**: Non-blocking operations for better performance

## 📦 Supported Devices

### SDM120 Energy Meter
- Voltage, current, power measurements
- Energy consumption tracking
- Demand monitoring
- Power factor and frequency

### PM2510-0D Dust Sensor
- PM2.5 and PM10 measurements
- Air quality monitoring
- Device configuration access

### XY-MD02 Environmental Sensor
- Temperature and humidity readings
- Environmental monitoring
- Signed temperature values with proper scaling

## 🛠️ Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/devonixcompany/MODBUSTCP.git
cd MODBUSTCP
```

2. Build and run with Docker Compose:
```bash
docker-compose up -d
```

### Manual Installation

1. Install Python 3.9+ and dependencies:
```bash
pip install -r requirements.txt
```

2. Install the package:
```bash
pip install -e .
```

## 🔧 Configuration

### Application Configuration

Copy and customize the configuration file:
```bash
cp config/config.yaml.example config/config.yaml
```

### Environment Variables

Copy and customize environment variables:
```bash
cp .env.example .env
```

### Device Configuration

Device configurations are stored in `config/devices/`. Templates are provided for:
- `sdm120.yaml` - Energy meter configuration
- `pm2510-0d.yaml` - Dust sensor configuration
- `xy-md02.yaml` - Environmental sensor configuration

## 📖 Usage

### Command Line Interface

The service provides a comprehensive CLI for device management:

```bash
# Show help
modbustcp --help

# Test connection to a device
modbustcp test-connection --host 10.1.2.1 --unit 1

# Add a device
modbustcp device add --name "Main Meter" --type SDM120 --host 10.1.2.1 --unit 1

# List all devices
modbustcp device list

# Connect to a device
modbustcp device connect <device-id>

# Collect data from a device
modbustcp data collect <device-id>

# Monitor device health
modbustcp monitor health <device-id>

# Start monitoring all devices
modbustcp monitor start <device-id>
```

### Docker Usage

```bash
# Run CLI commands in Docker
docker-compose exec modbustcp-service python -m presentation.cli.main device list

# View logs
docker-compose logs -f modbustcp-service

# Health check
docker-compose exec modbustcp-service python -m presentation.cli.main monitor health-all
```

## 🔍 Examples

### Adding and Monitoring an SDM120 Energy Meter

```bash
# Add the device
modbustcp device add \
  --name "Main Energy Meter" \
  --type SDM120 \
  --host 10.1.2.1 \
  --unit 1

# Get device ID from list
modbustcp device list

# Connect to the device
modbustcp device connect <device-id>

# Collect data
modbustcp data collect <device-id>

# Check latest readings
modbustcp data latest <device-id>

# Start monitoring
modbustcp monitor start <device-id> --interval 30
```

### Environmental Monitoring with XY-MD02

```bash
# Add temperature/humidity sensor
modbustcp device add \
  --name "Room Sensor" \
  --type XY-MD02 \
  --host 10.1.2.1 \
  --unit 2

# Monitor environmental conditions
modbustcp data collect <device-id>
modbustcp monitor health <device-id>
```

## 📊 Data Structure

### Device Entity
```python
@dataclass
class Device:
    id: DeviceId
    name: str
    device_type: DeviceType
    address: ModbusAddress
    unit_id: int
    status: DeviceStatus
```

### Reading Entity
```python
@dataclass
class Reading:
    device_id: DeviceId
    reading_type: ReadingType
    value: Union[float, int]
    unit: str
    timestamp: datetime
    register_address: int
    quality: Optional[str]
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test category
pytest tests/unit/
pytest tests/integration/
```

## 🔒 Production Deployment

### Docker Production Setup

1. Update configuration for production:
```yaml
# config/config.yaml
environment: "production"
debug: false
logging:
  level: "INFO"
  file: "/var/log/modbustcp/app.log"
```

2. Deploy with Docker Compose:
```bash
docker-compose -f docker-compose.yml up -d
```

### Security Considerations

- Run as non-root user (handled in Docker)
- Use environment variables for sensitive configuration
- Implement proper network security for MODBUS TCP connections
- Regular security updates for base images

### Monitoring and Logging

- Application logs: `/var/log/modbustcp/app.log`
- Health checks: Built-in Docker health checks
- Metrics: Device health and reading quality monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes following the clean architecture principles
4. Add tests for new functionality
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run linting
black src/
flake8 src/
mypy src/
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Contact: dev@devonixcompany.com

## 🔮 Roadmap

- [ ] REST API interface
- [ ] Web dashboard
- [ ] Database persistence (PostgreSQL/InfluxDB)
- [ ] Time-series data visualization
- [ ] Alerting and notifications
- [ ] Additional device drivers
- [ ] OPC-UA gateway functionality

## 📈 Migration from Legacy Scripts

If you're migrating from the original individual scripts:

### Original Scripts → New Architecture

- `sdm120_read.py` → Use SDM120 device configuration + CLI
- `pm2510_0d_summary.py` → Use PM2510-0D device configuration + CLI  
- `xy_md02_summary.py` → Use XY-MD02 device configuration + CLI

### Migration Steps

1. **Backup your existing scripts**
2. **Configure devices** using the new YAML configuration format
3. **Add devices** using the CLI: `modbustcp device add ...`
4. **Test connectivity** with: `modbustcp test-connection ...`
5. **Collect data** with: `modbustcp data collect ...`
6. **Setup monitoring** with: `modbustcp monitor start ...`

The new architecture provides the same functionality with improved:
- Error handling and logging
- Configuration management
- Monitoring and health checks
- Production readiness
- Maintainability and testability