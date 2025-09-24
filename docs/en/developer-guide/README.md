# Developer Guide

Technical documentation for developers who want to understand, extend, or contribute to the MODBUS TCP Service.

## 📋 Table of Contents

### Architecture & Design
- **[Architecture Overview](architecture.md)** - High-level system architecture
- **[Clean Architecture Principles](clean-architecture.md)** - Why and how we use clean architecture
- **[Domain Layer](domain-layer.md)** - Business entities and logic
- **[Application Layer](application-layer.md)** - Use cases and services
- **[Infrastructure Layer](infrastructure-layer.md)** - External concerns and implementations
- **[Presentation Layer](presentation-layer.md)** - User interfaces (CLI and API)

### Development
- **[Development Setup](development-setup.md)** - Set up your development environment
- **[Code Structure](code-structure.md)** - Understanding the codebase organization
- **[Adding New Devices](adding-devices.md)** - How to add support for new MODBUS devices
- **[Database Schema](database-schema.md)** - Database design and relationships
- **[API Design](api-design.md)** - REST API design principles

### Quality & Testing
- **[Testing Guide](testing.md)** - Testing strategies and practices
- **[Code Quality](code-quality.md)** - Linting, formatting, and best practices
- **[Performance](performance.md)** - Performance considerations and optimization

### Contributing
- **[Contributing Guidelines](contributing.md)** - How to contribute to the project
- **[Release Process](release-process.md)** - How releases are managed
- **[Troubleshooting Development](troubleshooting-dev.md)** - Common development issues

## 🏗️ Architecture Overview

The MODBUS TCP Service follows **Clean Architecture** principles with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐│
│  │        CLI          │  │         REST API                ││
│  │   (Click-based)     │  │   (FastAPI + Swagger)          ││
│  └─────────────────────┘  └─────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐│
│  │    Use Cases        │  │       Interfaces                ││
│  │ - DeviceManagement  │  │ - ModbusClient                  ││
│  │ - DataCollection    │  │ - Repositories                  ││
│  │ - Monitoring        │  │ - Configuration                 ││
│  └─────────────────────┘  └─────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                           │  
│  ┌─────────────────────┐  ┌─────────────────────────────────┐│
│  │     Entities        │  │       Value Objects             ││
│  │ - Device            │  │ - DeviceId                      ││
│  │ - Reading           │  │ - DeviceType                    ││
│  │ - DeviceConfig      │  │ - ModbusAddress                 ││
│  └─────────────────────┘  └─────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                      │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐│
│  │  MODBUS Client      │  │       Databases                 ││
│  │ - PyModbus TCP      │  │ - PostgreSQL                    ││
│  │ - Connection Pool   │  │ - InfluxDB                      ││
│  │ - Error Handling    │  │ - In-Memory (dev)               ││
│  └─────────────────────┘  └─────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Key Design Principles

### 1. Clean Architecture
- **Inner layers don't depend on outer layers**
- **Business logic is isolated from frameworks**
- **Easy to test and maintain**

### 2. Domain-Driven Design
- **Rich domain models** with business logic
- **Value objects** for type safety
- **Repository pattern** for data access abstraction

### 3. SOLID Principles
- **Single Responsibility** - Each class has one reason to change
- **Open/Closed** - Open for extension, closed for modification
- **Liskov Substitution** - Subtypes must be substitutable
- **Interface Segregation** - Many specific interfaces vs one general
- **Dependency Inversion** - Depend on abstractions, not concretions

### 4. Async/Await Pattern
- **Non-blocking I/O** for better performance
- **Concurrent operations** for multiple devices
- **Proper resource management**

## 🔧 Development Workflow

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/devonixcompany/MODBUSTCP.git
cd MODBUSTCP

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Install development tools
pip install pytest pytest-asyncio black flake8 mypy pre-commit
```

### 2. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_device_management.py

# Run async tests
pytest -k "async"
```

### 3. Code Quality

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/

# Run all quality checks
make quality  # If Makefile exists
```

### 4. Manual Testing

```bash
# Start development services
docker-compose -f docker-compose.dev.yml up -d

# Test CLI
python modbustcp.py --help

# Test API
python api_server.py
curl http://localhost:8000/api/v1/health
```

## 📦 Project Structure

```
MODBUSTCP/
├── src/                          # Source code
│   ├── domain/                   # Business logic
│   │   ├── entities/            # Core business entities
│   │   ├── value_objects/       # Immutable value objects
│   │   └── repositories/        # Repository interfaces
│   ├── application/              # Use cases and services
│   │   ├── use_cases/           # Business use cases
│   │   └── interfaces/          # Infrastructure interfaces
│   ├── infrastructure/           # External concerns
│   │   ├── modbus/              # MODBUS implementation
│   │   ├── database/            # Database implementations
│   │   └── config/              # Configuration management
│   └── presentation/             # User interfaces
│       ├── cli/                 # CLI interface
│       └── api/                 # REST API
├── tests/                        # Test files
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── fixtures/                # Test fixtures
├── docs/                         # Documentation
├── config/                       # Configuration files
├── migrations/                   # Database migrations
├── scripts/                      # Utility scripts
├── docker-compose.yml           # Docker composition
├── Dockerfile                   # Container definition
├── requirements.txt             # Python dependencies
└── setup.py                     # Package setup
```

## 🧪 Testing Strategy

### Unit Tests
- **Domain entities** - Business logic validation
- **Value objects** - Immutability and validation
- **Use cases** - Business use case logic
- **Repositories** - Data access patterns

### Integration Tests
- **Database integration** - Repository implementations
- **MODBUS communication** - Device connectivity
- **API endpoints** - HTTP request/response
- **CLI commands** - Command-line interface

### End-to-End Tests
- **Complete workflows** - Full user scenarios
- **Docker integration** - Container deployments
- **Performance tests** - Load and stress testing

## 🚀 Adding New Features

### 1. New MODBUS Device Type

1. **Define device characteristics** in domain layer
2. **Create device configuration** template
3. **Implement register mappings**
4. **Add tests** for the new device
5. **Update documentation**

See: [Adding New Devices](adding-devices.md)

### 2. New API Endpoint

1. **Define request/response schemas** in presentation layer
2. **Implement business logic** in application layer
3. **Add routing** in API router
4. **Write tests** for the endpoint
5. **Update API documentation**

### 3. New Database Support

1. **Implement repository interface** in infrastructure layer
2. **Add database-specific logic**
3. **Create migration scripts**
4. **Add configuration options**
5. **Test with existing use cases**

## 📊 Performance Considerations

### MODBUS Communication
- **Connection pooling** for multiple devices
- **Concurrent requests** with async/await
- **Timeout handling** and retries
- **Register batching** for efficiency

### Database Operations
- **Connection pooling** for database access
- **Batch operations** for multiple inserts
- **Indexing strategy** for queries
- **Query optimization**

### Memory Management
- **Lazy loading** for large datasets
- **Resource cleanup** with context managers
- **Garbage collection** optimization

## 🔐 Security Considerations

### Code Security
- **Input validation** at all entry points
- **SQL injection prevention** with parameterized queries
- **Configuration security** (no hardcoded secrets)
- **Dependency scanning** for vulnerabilities

### Network Security
- **MODBUS protocol security** considerations
- **TLS/SSL** for API endpoints (when implemented)
- **Network segmentation** recommendations

## 📖 Learning Resources

### Clean Architecture
- [Clean Architecture Book](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164) by Robert C. Martin
- [Clean Architecture in Python](https://www.cosmicpython.com/) by Harry Percival

### MODBUS Protocol
- [MODBUS Specification](https://modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf)
- [PyModbus Documentation](https://pymodbus.readthedocs.io/)

### Python Best Practices
- [Python Enhancement Proposals (PEPs)](https://www.python.org/dev/peps/)
- [Real Python](https://realpython.com/) tutorials
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 🤝 Getting Involved

### Ways to Contribute
1. **Report bugs** and issues
2. **Suggest features** and improvements
3. **Submit pull requests** with fixes or features
4. **Improve documentation**
5. **Write tests** and improve coverage
6. **Performance optimization**

### Development Process
1. **Fork** the repository
2. **Create feature branch** from main
3. **Make changes** following coding standards
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Submit pull request** with clear description

## 🛠️ Tools and Technologies

### Core Technologies
- **Python 3.11+** - Primary language
- **FastAPI** - REST API framework
- **SQLAlchemy** - ORM for database access
- **Alembic** - Database migrations
- **PyModbus** - MODBUS protocol implementation
- **Click** - CLI framework

### Development Tools
- **pytest** - Testing framework
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking
- **pre-commit** - Git hooks

### Infrastructure
- **PostgreSQL** - Relational database
- **InfluxDB** - Time-series database
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📞 Support

For development-related questions:

1. **Check existing documentation** in this guide
2. **Search [GitHub Issues](https://github.com/devonixcompany/MODBUSTCP/issues)**
3. **Review code examples** in the repository
4. **Ask questions** in GitHub Discussions
5. **Submit issues** for bugs or feature requests

Ready to start developing? Begin with [Development Setup](development-setup.md)!