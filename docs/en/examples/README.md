# Examples

Practical examples and tutorials for using the MODBUS TCP Service.

## 📋 Table of Contents

### Basic Usage
- **[Basic Usage Examples](basic-usage.md)** - Fundamental operations
- **[CLI Examples](cli-examples.md)** - Command-line interface examples
- **[API Examples](api-examples.md)** - REST API usage examples

### Device Configuration
- **[Device Configuration Examples](device-configs.md)** - Pre-configured device templates
- **[Custom Device Setup](custom-devices.md)** - Creating configurations for new devices
- **[Register Mapping](register-mapping.md)** - Understanding MODBUS register mappings

### Integration
- **[Integration Examples](integrations.md)** - Integrating with external systems
- **[Data Export Examples](data-export.md)** - Exporting data to different formats
- **[Monitoring Integration](monitoring-integration.md)** - Integration with monitoring tools

### Advanced Usage
- **[Batch Operations](batch-operations.md)** - Processing multiple devices
- **[Automation Scripts](automation-scripts.md)** - Automated data collection
- **[Performance Optimization](performance-examples.md)** - Optimizing for scale

## 🚀 Quick Examples

### 1. Add and Test a Device

**CLI:**
```bash
# Add SDM120 energy meter
python modbustcp.py device add \
  --name "Main Meter" \
  --type SDM120 \
  --host 192.168.1.100 \
  --unit 1

# Test connection
python modbustcp.py test-connection --host 192.168.1.100 --unit 1

# List devices
python modbustcp.py device list
```

**API:**
```bash
# Add device via REST API
curl -X POST "http://localhost:8000/api/v1/devices" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Main Meter",
       "device_type": "SDM120",
       "host": "192.168.1.100",
       "unit_id": 1,
       "timeout": 3
     }'

# Test connection
curl -X POST "http://localhost:8000/api/v1/devices/test-connection" \
     -H "Content-Type: application/json" \
     -d '{
       "host": "192.168.1.100",
       "unit_id": 1,
       "timeout": 3
     }'
```

### 2. Collect Data

**CLI:**
```bash
# Collect from specific device
python modbustcp.py data collect <device-id>

# Collect from all devices
python modbustcp.py data collect-all

# View latest readings
python modbustcp.py data latest <device-id>
```

**API:**
```bash
# Collect data
curl -X POST "http://localhost:8000/api/v1/readings/collect" \
     -H "Content-Type: application/json" \
     -d '{"device_id": "your-device-id"}'

# Get latest readings
curl "http://localhost:8000/api/v1/readings/latest/your-device-id"
```

### 3. Monitor Health

**CLI:**
```bash
# Check all devices
python modbustcp.py monitor health-all

# Start continuous monitoring
python modbustcp.py monitor start <device-id> --interval 30
```

**API:**
```bash
# System health overview
curl "http://localhost:8000/api/v1/monitoring/system-health"

# All devices health
curl "http://localhost:8000/api/v1/monitoring/health"
```

## 🔧 Device Type Examples

### SDM120 Energy Meter

**Configuration:**
```yaml
name: "Building Main Meter"
type: "SDM120"
address:
  host: "192.168.1.100"
  port: 502
unit_id: 1
timeout: 3
registers:
  - name: "voltage"
    address: 0x0000
    data_type: "float32"
    unit: "V"
  - name: "current"
    address: 0x0006
    data_type: "float32"
    unit: "A"
  - name: "power"
    address: 0x000C
    data_type: "float32"
    unit: "W"
```

**Expected Readings:**
```json
{
  "readings": [
    {
      "reading_type": "voltage",
      "value": 230.5,
      "unit": "V",
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "reading_type": "current",
      "value": 12.3,
      "unit": "A",
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "reading_type": "power",
      "value": 2835.0,
      "unit": "W",
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### PM2510-0D Dust Sensor

**Configuration:**
```yaml
name: "Air Quality Monitor"
type: "PM2510-0D"
address:
  host: "192.168.1.101"
  port: 502
unit_id: 4
timeout: 3
registers:
  - name: "pm25"
    address: 0x0004
    data_type: "uint16"
    unit: "µg/m³"
  - name: "pm10"
    address: 0x0009
    data_type: "uint16"
    unit: "µg/m³"
```

**Expected Readings:**
```json
{
  "readings": [
    {
      "reading_type": "pm25",
      "value": 35,
      "unit": "µg/m³",
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "reading_type": "pm10",
      "value": 55,
      "unit": "µg/m³",
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### XY-MD02 Environmental Sensor

**Configuration:**
```yaml
name: "Environment Monitor"
type: "XY-MD02"
address:
  host: "192.168.1.102"
  port: 502
unit_id: 2
timeout: 3
registers:
  - name: "temperature"
    address: 0x0001
    data_type: "int16"
    unit: "°C"
    scale_factor: 0.1
  - name: "humidity"
    address: 0x0002
    data_type: "uint16"
    unit: "%RH"
    scale_factor: 0.1
```

**Expected Readings:**
```json
{
  "readings": [
    {
      "reading_type": "temperature",
      "value": 23.5,
      "unit": "°C",
      "timestamp": "2024-01-01T12:00:00Z"
    },
    {
      "reading_type": "humidity",
      "value": 65.2,
      "unit": "%RH",
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```

## 🐍 Python Integration Examples

### Basic Device Management

```python
import requests
import json

class ModbusAPI:
    def __init__(self, base_url="http://localhost:8000/api/v1"):
        self.base_url = base_url
    
    def add_device(self, name, device_type, host, unit_id):
        """Add a new MODBUS device."""
        data = {
            "name": name,
            "device_type": device_type,
            "host": host,
            "unit_id": unit_id,
            "timeout": 3
        }
        response = requests.post(f"{self.base_url}/devices", json=data)
        return response.json()
    
    def get_devices(self):
        """Get all devices."""
        response = requests.get(f"{self.base_url}/devices")
        return response.json()
    
    def collect_data(self, device_id):
        """Collect data from a device."""
        data = {"device_id": device_id}
        response = requests.post(f"{self.base_url}/readings/collect", json=data)
        return response.json()
    
    def get_latest_readings(self, device_id):
        """Get latest readings for a device."""
        response = requests.get(f"{self.base_url}/readings/latest/{device_id}")
        return response.json()

# Usage example
api = ModbusAPI()

# Add device
device = api.add_device("Test Meter", "SDM120", "192.168.1.100", 1)
device_id = device["id"]

# Collect data
result = api.collect_data(device_id)
print(f"Collected {result['readings_collected']} readings")

# Get readings
readings = api.get_latest_readings(device_id)
for reading in readings:
    print(f"{reading['reading_type']}: {reading['value']} {reading['unit']}")
```

### Async Data Collection

```python
import asyncio
import aiohttp
import json

class AsyncModbusAPI:
    def __init__(self, base_url="http://localhost:8000/api/v1"):
        self.base_url = base_url
    
    async def collect_all_devices(self):
        """Collect data from all devices concurrently."""
        async with aiohttp.ClientSession() as session:
            # Get all devices
            async with session.get(f"{self.base_url}/devices") as response:
                devices = await response.json()
            
            # Collect data from all devices concurrently
            tasks = []
            for device in devices["devices"]:
                task = self.collect_device_data(session, device["id"])
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            return results
    
    async def collect_device_data(self, session, device_id):
        """Collect data from a single device."""
        data = {"device_id": device_id}
        async with session.post(
            f"{self.base_url}/readings/collect",
            json=data
        ) as response:
            return await response.json()

# Usage example
async def main():
    api = AsyncModbusAPI()
    results = await api.collect_all_devices()
    
    for result in results:
        print(f"Device {result['device_id']}: {result['readings_collected']} readings")

# Run
asyncio.run(main())
```

## 🌐 Web Integration Examples

### JavaScript/Browser Integration

```html
<!DOCTYPE html>
<html>
<head>
    <title>MODBUS Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div id="dashboard">
        <h1>MODBUS Device Dashboard</h1>
        <div id="devices"></div>
        <canvas id="chart"></canvas>
    </div>

    <script>
        class ModbusDashboard {
            constructor(apiUrl = 'http://localhost:8000/api/v1') {
                this.apiUrl = apiUrl;
                this.chart = null;
            }
            
            async loadDevices() {
                const response = await fetch(`${this.apiUrl}/devices`);
                const data = await response.json();
                return data.devices;
            }
            
            async getDeviceReadings(deviceId) {
                const response = await fetch(`${this.apiUrl}/readings/latest/${deviceId}`);
                return await response.json();
            }
            
            async renderDashboard() {
                const devices = await this.loadDevices();
                const container = document.getElementById('devices');
                
                for (const device of devices) {
                    const readings = await this.getDeviceReadings(device.id);
                    
                    const deviceDiv = document.createElement('div');
                    deviceDiv.innerHTML = `
                        <h3>${device.name} (${device.device_type})</h3>
                        <div class="readings">
                            ${readings.map(r => 
                                `<p>${r.reading_type}: ${r.value} ${r.unit}</p>`
                            ).join('')}
                        </div>
                    `;
                    container.appendChild(deviceDiv);
                }
            }
            
            async collectData() {
                const devices = await this.loadDevices();
                
                for (const device of devices) {
                    await fetch(`${this.apiUrl}/readings/collect`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ device_id: device.id })
                    });
                }
                
                this.renderDashboard();
            }
        }
        
        // Initialize dashboard
        const dashboard = new ModbusDashboard();
        dashboard.renderDashboard();
        
        // Auto-refresh every 30 seconds
        setInterval(() => dashboard.collectData(), 30000);
    </script>
</body>
</html>
```

## 🔄 Automation Examples

### Cron Job for Data Collection

```bash
#!/bin/bash
# collect_data.sh - Automated data collection script

# Set paths
SCRIPT_DIR="/path/to/MODBUSTCP"
LOG_FILE="/var/log/modbus_collection.log"

# Change to script directory
cd "$SCRIPT_DIR"

# Collect data from all devices
echo "[$(date)] Starting data collection" >> "$LOG_FILE"
python modbustcp.py data collect-all >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date)] Data collection successful" >> "$LOG_FILE"
else
    echo "[$(date)] Data collection failed with exit code $?" >> "$LOG_FILE"
fi
```

**Crontab entry:**
```bash
# Collect data every 5 minutes
*/5 * * * * /path/to/collect_data.sh

# Health check every hour
0 * * * * cd /path/to/MODBUSTCP && python modbustcp.py monitor health-all
```

### Python Automation Script

```python
#!/usr/bin/env python3
"""
Automated MODBUS data collection and monitoring script.
"""

import time
import logging
import requests
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('modbus_automation.log'),
        logging.StreamHandler()
    ]
)

class ModbusAutomation:
    def __init__(self, api_url="http://localhost:8000/api/v1"):
        self.api_url = api_url
        self.logger = logging.getLogger(__name__)
    
    def check_health(self):
        """Check system health."""
        try:
            response = requests.get(f"{self.api_url}/monitoring/system-health")
            health = response.json()
            
            self.logger.info(f"System Health: {health['status']}")
            self.logger.info(f"Total devices: {health['total_devices']}")
            self.logger.info(f"Healthy devices: {health['healthy_devices']}")
            
            return health['status'] == 'healthy'
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    def collect_all_data(self):
        """Collect data from all devices."""
        try:
            response = requests.post(f"{self.api_url}/readings/collect-all")
            results = response.json()
            
            total_readings = sum(r['readings_collected'] for r in results)
            self.logger.info(f"Collected {total_readings} total readings")
            
            return True
        except Exception as e:
            self.logger.error(f"Data collection failed: {e}")
            return False
    
    def run_cycle(self):
        """Run one automation cycle."""
        self.logger.info("Starting automation cycle")
        
        # Check health first
        if not self.check_health():
            self.logger.warning("System health check failed")
            return False
        
        # Collect data
        if not self.collect_all_data():
            self.logger.error("Data collection failed")
            return False
        
        self.logger.info("Automation cycle completed successfully")
        return True
    
    def run_continuous(self, interval=300):  # 5 minutes
        """Run continuous automation."""
        self.logger.info(f"Starting continuous automation (interval: {interval}s)")
        
        while True:
            try:
                self.run_cycle()
                time.sleep(interval)
            except KeyboardInterrupt:
                self.logger.info("Automation stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    automation = ModbusAutomation()
    automation.run_continuous()
```

## 📊 Data Processing Examples

### Data Analysis with Pandas

```python
import pandas as pd
import requests
from datetime import datetime, timedelta

def get_device_data(device_id, hours=24):
    """Get historical data for analysis."""
    start_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat() + 'Z'
    
    response = requests.get(
        f"http://localhost:8000/api/v1/readings",
        params={
            'device_id': device_id,
            'start_time': start_time,
            'per_page': 1000
        }
    )
    
    data = response.json()
    return pd.DataFrame(data['readings'])

def analyze_energy_meter(device_id):
    """Analyze energy meter data."""
    df = get_device_data(device_id)
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Pivot data by reading type
    pivot_df = df.pivot(index='timestamp', columns='reading_type', values='value')
    
    # Calculate statistics
    stats = {
        'avg_voltage': pivot_df['voltage'].mean(),
        'avg_current': pivot_df['current'].mean(),
        'max_power': pivot_df['power'].max(),
        'total_energy_change': pivot_df['total_energy'].max() - pivot_df['total_energy'].min()
    }
    
    return stats, pivot_df

# Usage
device_id = "your-device-id"
stats, data = analyze_energy_meter(device_id)

print("Energy Meter Analysis:")
for key, value in stats.items():
    print(f"  {key}: {value:.2f}")
```

## 🔗 Integration Examples

### Grafana Dashboard

```yaml
# docker-compose.yml addition for Grafana
version: '3.8'
services:
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - influxdb

volumes:
  grafana_data:
```

### Home Assistant Integration

```yaml
# configuration.yaml
sensor:
  - platform: rest
    name: "Modbus Energy Meter"
    resource: "http://localhost:8000/api/v1/readings/latest/device-id"
    json_attributes:
      - readings
    value_template: "{{ value_json.readings | length }}"
    
  - platform: template
    sensors:
      voltage:
        friendly_name: "Voltage"
        value_template: >
          {% for reading in state_attr('sensor.modbus_energy_meter', 'readings') %}
            {% if reading.reading_type == 'voltage' %}
              {{ reading.value }}
            {% endif %}
          {% endfor %}
        unit_of_measurement: "V"
```

## 📱 Mobile App Integration

### React Native Example

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, RefreshControl } from 'react-native';

const ModbusDevices = () => {
  const [devices, setDevices] = useState([]);
  const [refreshing, setRefreshing] = useState(false);
  
  const API_URL = 'http://your-server:8000/api/v1';
  
  const loadDevices = async () => {
    try {
      const response = await fetch(`${API_URL}/devices`);
      const data = await response.json();
      setDevices(data.devices);
    } catch (error) {
      console.error('Failed to load devices:', error);
    }
  };
  
  const loadDeviceReadings = async (deviceId) => {
    try {
      const response = await fetch(`${API_URL}/readings/latest/${deviceId}`);
      const readings = await response.json();
      return readings;
    } catch (error) {
      console.error('Failed to load readings:', error);
      return [];
    }
  };
  
  const onRefresh = async () => {
    setRefreshing(true);
    await loadDevices();
    setRefreshing(false);
  };
  
  useEffect(() => {
    loadDevices();
  }, []);
  
  const renderDevice = ({ item }) => (
    <View style={{ padding: 16, borderBottomWidth: 1 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold' }}>{item.name}</Text>
      <Text>Type: {item.device_type}</Text>
      <Text>Status: {item.status}</Text>
      <Text>Host: {item.host}:{item.port}</Text>
    </View>
  );
  
  return (
    <FlatList
      data={devices}
      renderItem={renderDevice}
      keyExtractor={item => item.id}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    />
  );
};

export default ModbusDevices;
```

## 🔧 Troubleshooting Examples

See detailed troubleshooting examples in the [User Guide](../user-guide/troubleshooting.md).

## 📖 More Examples

For additional examples, check out:
- **[Basic Usage Examples](basic-usage.md)** - Simple operations
- **[Device Configuration Examples](device-configs.md)** - Device setup
- **[Integration Examples](integrations.md)** - External system integration
- **[Performance Examples](performance-examples.md)** - Optimization techniques

Ready to try these examples? Start with [Basic Usage Examples](basic-usage.md)!