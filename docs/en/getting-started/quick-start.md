# Quick Start Guide

Get the MODBUS TCP Service running in under 5 minutes using Docker.

## 🚀 Step 1: Clone the Repository

```bash
git clone https://github.com/devonixcompany/MODBUSTCP.git
cd MODBUSTCP
```

## 🐳 Step 2: Start with Docker Compose

The fastest way to get everything running:

```bash
# Start all services (API, PostgreSQL, InfluxDB)
docker-compose up -d

# Check if services are running
docker-compose ps
```

This will start:
- **MODBUS TCP API** on `http://localhost:8000`
- **PostgreSQL** database on port `5432`
- **InfluxDB** on port `8086`

## 🌐 Step 3: Access the API

Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## 🔧 Step 4: Add Your First Device

### Using the Web Interface (Swagger UI)

1. Go to http://localhost:8000/docs
2. Click on **"POST /api/v1/devices"**
3. Click **"Try it out"**
4. Use this example configuration:

```json
{
  "name": "My Energy Meter",
  "device_type": "SDM120",
  "host": "10.1.2.1",
  "port": 502,
  "unit_id": 1,
  "timeout": 3
}
```

5. Click **"Execute"**

### Using the Command Line

```bash
# Enter the API container
docker-compose exec modbustcp-api bash

# Add a device
python modbustcp.py device add \
  --name "My Energy Meter" \
  --type SDM120 \
  --host 10.1.2.1 \
  --unit 1

# List devices
python modbustcp.py device list
```

## 📊 Step 5: Test Connection

Before collecting data, test the connection:

### Using the API

1. In Swagger UI, find **"POST /api/v1/devices/test-connection"**
2. Test with your device settings:

```json
{
  "host": "10.1.2.1",
  "port": 502,
  "unit_id": 1,
  "timeout": 3
}
```

### Using the CLI

```bash
# Test connection
python modbustcp.py test-connection --host 10.1.2.1 --unit 1
```

## 📈 Step 6: Collect Data

Once your device is connected:

### Using the API

1. Find **"POST /api/v1/readings/collect"**
2. Use your device ID to collect data:

```json
{
  "device_id": "your-device-id"
}
```

### Using the CLI

```bash
# Collect data from a specific device
python modbustcp.py data collect <device-id>

# Collect from all devices
python modbustcp.py data collect-all
```

## 🏥 Step 7: Monitor Health

Check the health of your devices:

### Using the API

- **Single device**: GET `/api/v1/monitoring/health/{device_id}`
- **All devices**: GET `/api/v1/monitoring/health`
- **System overview**: GET `/api/v1/monitoring/system-health`

### Using the CLI

```bash
# Check all devices
python modbustcp.py monitor health-all

# Check specific device
python modbustcp.py monitor health <device-id>
```

## 🎯 Next Steps

Congratulations! You now have a running MODBUS TCP service. Here's what to do next:

### Explore the Features
- **[Device Management](../user-guide/device-management.md)** - Learn about device configuration
- **[Data Collection](../user-guide/data-collection.md)** - Understand data collection options
- **[API Reference](../api-reference/)** - Explore all API endpoints

### Configure for Your Environment
- **[Configuration Guide](configuration.md)** - Customize settings
- **[Device Templates](../examples/device-configs.md)** - Pre-built device configurations

### Production Deployment
- **[Environment Configuration](../deployment/environment.md)** - Production settings
- **[Security](../deployment/security.md)** - Security considerations
- **[Monitoring](../deployment/monitoring.md)** - Production monitoring

## 🛑 Troubleshooting

### Common Issues

**Services won't start?**
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose down
docker-compose up -d
```

**Can't connect to device?**
```bash
# Check network connectivity
ping 10.1.2.1

# Verify MODBUS settings
python modbustcp.py test-connection --host 10.1.2.1 --unit 1
```

**Database connection issues?**
```bash
# Check database logs
docker-compose logs postgres
docker-compose logs influxdb

# Reset databases
docker-compose down -v
docker-compose up -d
```

For more help, see the **[Troubleshooting Guide](../user-guide/troubleshooting.md)**.

## 🎉 Success!

You now have a fully functional MODBUS TCP service with:
- ✅ REST API with Swagger documentation
- ✅ Database persistence (PostgreSQL + InfluxDB)
- ✅ Device management capabilities
- ✅ Data collection and monitoring
- ✅ Health checks and system status

Ready to explore more features? Check out the **[User Guide](../user-guide/)** or **[API Reference](../api-reference/)**!