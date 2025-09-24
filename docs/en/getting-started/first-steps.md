# First Steps

Now that you have the MODBUS TCP Service installed, let's walk through the basic operations to get you started.

## 🎯 Overview

In this guide, you'll learn to:
1. Test your installation
2. Add your first MODBUS device
3. Collect data from the device
4. Monitor device health
5. View collected data

## 🧪 Step 1: Test Your Installation

First, let's make sure everything is working properly.

### Test CLI Interface

```bash
# Check if the CLI is working
python modbustcp.py --help

# Check system status
python modbustcp.py info
```

### Test API Interface

```bash
# Start the API server (if not using Docker)
python api_server.py &

# Test API health
curl http://localhost:8000/api/v1/health

# Open Swagger UI in browser
open http://localhost:8000/docs
```

## 🔧 Step 2: Add Your First Device

Let's add a MODBUS device to the system. We'll use an SDM120 energy meter as an example.

### Using CLI

```bash
# Add an SDM120 energy meter
python modbustcp.py device add \
  --name "Main Energy Meter" \
  --type SDM120 \
  --host 10.1.2.1 \
  --unit 1 \
  --timeout 3

# List all devices to see your new device
python modbustcp.py device list
```

### Using API (Swagger UI)

1. Go to http://localhost:8000/docs
2. Find the **"POST /api/v1/devices"** endpoint
3. Click **"Try it out"**
4. Use this JSON configuration:

```json
{
  "name": "Main Energy Meter",
  "device_type": "SDM120",
  "host": "10.1.2.1",
  "port": 502,
  "unit_id": 1,
  "timeout": 3
}
```

5. Click **"Execute"**

### Supported Device Types

| Type | Description | Typical Use |
|------|-------------|-------------|
| `SDM120` | Energy meter | Voltage, current, power monitoring |
| `PM2510-0D` | Dust sensor | Air quality monitoring |
| `XY-MD02` | Environmental sensor | Temperature and humidity |
| `GENERIC` | Custom device | Any MODBUS device |

## 🔌 Step 3: Test Device Connection

Before collecting data, test if you can connect to your device.

### Using CLI

```bash
# Test connection to specific device
python modbustcp.py test-connection --host 10.1.2.1 --unit 1

# Test all configured devices
python modbustcp.py device test-all
```

### Using API

Use the **"POST /api/v1/devices/test-connection"** endpoint with:

```json
{
  "host": "10.1.2.1",
  "port": 502,
  "unit_id": 1,
  "timeout": 3
}
```

### Troubleshooting Connection Issues

**Connection timeout:**
```bash
# Increase timeout
python modbustcp.py test-connection --host 10.1.2.1 --unit 1 --timeout 10

# Check network connectivity
ping 10.1.2.1
```

**Wrong unit ID:**
```bash
# Try different unit IDs
for unit in {1..10}; do
  echo "Testing unit $unit"
  python modbustcp.py test-connection --host 10.1.2.1 --unit $unit
done
```

## 📊 Step 4: Collect Your First Data

Once your device connects successfully, collect some data.

### Using CLI

```bash
# Get your device ID first
python modbustcp.py device list

# Collect data using device ID
python modbustcp.py data collect <device-id>

# Or collect from all devices
python modbustcp.py data collect-all
```

### Using API

1. Go to **"POST /api/v1/readings/collect"**
2. Use your device ID:

```json
{
  "device_id": "your-device-id"
}
```

### What Data Is Collected?

For an **SDM120 device**, you'll see readings like:
- Voltage (V)
- Current (A)
- Active Power (W)
- Frequency (Hz)
- Total Energy (kWh)

For a **PM2510-0D device**:
- PM2.5 (µg/m³)
- PM10 (µg/m³)

For an **XY-MD02 device**:
- Temperature (°C)
- Humidity (%RH)

## 📈 Step 5: View Collected Data

Now let's look at the data you've collected.

### Using CLI

```bash
# View latest readings for a device
python modbustcp.py data latest <device-id>

# View historical data
python modbustcp.py data history <device-id> --hours 24

# View statistics
python modbustcp.py data statistics <device-id>
```

### Using API

**Latest readings:** GET `/api/v1/readings/latest/{device_id}`

**Historical data:** GET `/api/v1/readings?device_id={device_id}&start_time=2024-01-01T00:00:00Z`

**Statistics:** GET `/api/v1/readings/statistics/{device_id}`

## 🏥 Step 6: Monitor Device Health

Keep track of your devices' health and connectivity.

### Using CLI

```bash
# Check health of all devices
python modbustcp.py monitor health-all

# Check specific device health
python modbustcp.py monitor health <device-id>

# Start continuous monitoring
python modbustcp.py monitor start <device-id>
```

### Using API

**All devices health:** GET `/api/v1/monitoring/health`

**Single device:** GET `/api/v1/monitoring/health/{device_id}`

**System overview:** GET `/api/v1/monitoring/system-health`

### Understanding Health Status

| Status | Meaning | Action |
|--------|---------|--------|
| `healthy` | Device responding normally | None needed |
| `warning` | Minor issues detected | Monitor closely |
| `error` | Connection problems | Check network/device |
| `disconnected` | No connection | Verify device is online |

## 🔄 Step 7: Automate Data Collection

Set up automatic data collection for continuous monitoring.

### Using CLI with Scheduling

```bash
# Start monitoring with 30-second interval
python modbustcp.py monitor start <device-id> --interval 30

# Stop monitoring
python modbustcp.py monitor stop <device-id>
```

### Using API

**Start monitoring:** POST `/api/v1/monitoring/start`

```json
{
  "device_id": "your-device-id",
  "interval": 30
}
```

**Stop monitoring:** POST `/api/v1/monitoring/stop/{device_id}`

### Using System Cron (Linux/macOS)

```bash
# Edit crontab
crontab -e

# Add entry to collect data every 5 minutes
*/5 * * * * cd /path/to/MODBUSTCP && python modbustcp.py data collect-all
```

## 📊 Step 8: Explore the Web Interface

The Swagger UI provides a comprehensive web interface for the API.

### Access Swagger UI

1. Go to http://localhost:8000/docs
2. Explore different endpoint categories:
   - **Health** - System status
   - **Devices** - Device management
   - **Readings** - Data collection
   - **Monitoring** - Health monitoring

### Try Interactive Examples

1. Click on any endpoint
2. Click **"Try it out"**
3. Modify the example data
4. Click **"Execute"**
5. See the response

## 🎯 What's Next?

Congratulations! You've successfully:
- ✅ Added your first MODBUS device
- ✅ Tested connectivity
- ✅ Collected data
- ✅ Monitored device health
- ✅ Explored the web interface

### Continue Learning

- **[Device Management](../user-guide/device-management.md)** - Advanced device configuration
- **[Configuration Management](../user-guide/configuration.md)** - Custom device settings
- **[API Reference](../api-reference/)** - Complete API documentation
- **[Examples](../examples/)** - More practical examples

### Production Deployment

Ready for production? Check out:
- **[Environment Configuration](../deployment/environment.md)**
- **[Security Considerations](../deployment/security.md)**
- **[Monitoring & Logging](../deployment/monitoring.md)**

## 🛟 Need Help?

Stuck? Here are some resources:
- **[Troubleshooting Guide](../user-guide/troubleshooting.md)**
- **[User Guide](../user-guide/)** - Comprehensive documentation
- **GitHub Issues** - Report bugs or ask questions

## 🔧 Common Next Steps

Based on your use case:

**For IoT Projects:**
- Set up automated data collection
- Configure InfluxDB for time-series data
- Implement data visualization

**For Industrial Monitoring:**
- Add multiple devices
- Set up health monitoring alerts  
- Configure backup and redundancy

**For Development:**
- Explore the codebase architecture
- Add custom device types
- Contribute to the project

Ready to dive deeper? Choose your path and continue exploring! 🚀