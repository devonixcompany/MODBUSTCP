# API Reference

Complete documentation for the MODBUS TCP Service REST API.

## 📋 Table of Contents

### Getting Started
- **[API Overview](overview.md)** - Introduction to the REST API
- **[Authentication](authentication.md)** - API security and authentication
- **[Quick Start](quick-start.md)** - Get started with the API in minutes

### Endpoint References
- **[Device Endpoints](devices.md)** - Device management operations
- **[Reading Endpoints](readings.md)** - Data collection and retrieval
- **[Monitoring Endpoints](monitoring.md)** - Health checks and system status
- **[System Endpoints](system.md)** - Service information and utilities

### API Details
- **[Request/Response Format](format.md)** - Data structures and conventions
- **[Error Handling](errors.md)** - Error codes and handling
- **[Rate Limiting](rate-limiting.md)** - API usage limits
- **[Pagination](pagination.md)** - Handling large datasets

### Interactive Documentation
- **[OpenAPI Specification](openapi.md)** - Machine-readable API spec
- **[Swagger UI Guide](swagger-ui.md)** - Using the interactive documentation

## 🌐 Base URL

The API is accessible at the following base URL:

```
http://localhost:8000/api/v1
```

In production, replace `localhost:8000` with your actual server address.

## 📊 Quick Reference

### Authentication
```bash
# Currently no authentication required
# Future versions will support API keys or JWT tokens
curl -H "Content-Type: application/json" \
     http://localhost:8000/api/v1/health
```

### Common HTTP Methods

| Method | Usage | Example |
|--------|-------|---------|
| `GET` | Retrieve data | Get device list |
| `POST` | Create new resource | Add new device |
| `PUT` | Update existing resource | Update device settings |
| `DELETE` | Remove resource | Delete device |

### Response Formats

All API responses use JSON format:

```json
{
  "status": "success",
  "data": {
    // Response data here
  },
  "message": "Operation completed successfully"
}
```

## 🔗 Endpoint Categories

### 🏥 Health & Status
Check system health and service status.

```bash
GET /api/v1/health                 # API health check
GET /api/v1/monitoring/system-health # System overview
```

### 🔧 Device Management
Manage MODBUS devices in your system.

```bash
GET    /api/v1/devices              # List all devices
POST   /api/v1/devices              # Add new device
GET    /api/v1/devices/{id}         # Get device details
PUT    /api/v1/devices/{id}         # Update device
DELETE /api/v1/devices/{id}         # Delete device
```

### 📊 Data Collection
Collect and retrieve sensor readings.

```bash
GET  /api/v1/readings               # List readings
POST /api/v1/readings/collect       # Collect data
GET  /api/v1/readings/latest/{id}   # Latest readings
GET  /api/v1/readings/statistics/{id} # Data statistics
```

### 🏥 Monitoring
Monitor device health and system status.

```bash
GET  /api/v1/monitoring/health      # All devices health
GET  /api/v1/monitoring/health/{id} # Single device health
POST /api/v1/monitoring/start       # Start monitoring
POST /api/v1/monitoring/stop/{id}   # Stop monitoring
```

## 🚀 Interactive Documentation

The API provides interactive documentation through Swagger UI:

### Access Swagger UI
1. Start the API server: `python api_server.py`
2. Open: http://localhost:8000/docs
3. Explore and test endpoints interactively

### Features
- **Try it out** - Test endpoints directly from the browser
- **Request/Response examples** - See expected data formats
- **Schema documentation** - Understand data structures
- **Authentication testing** - Test with different credentials

## 📝 Example Usage

### Basic Device Operations

**Add a new device:**
```bash
curl -X POST "http://localhost:8000/api/v1/devices" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Main Energy Meter",
       "device_type": "SDM120",
       "host": "10.1.2.1",
       "port": 502,
       "unit_id": 1,
       "timeout": 3
     }'
```

**List all devices:**
```bash
curl "http://localhost:8000/api/v1/devices"
```

**Get device details:**
```bash
curl "http://localhost:8000/api/v1/devices/{device-id}"
```

### Data Collection

**Collect readings:**
```bash
curl -X POST "http://localhost:8000/api/v1/readings/collect" \
     -H "Content-Type: application/json" \
     -d '{"device_id": "your-device-id"}'
```

**Get latest readings:**
```bash
curl "http://localhost:8000/api/v1/readings/latest/{device-id}"
```

### Health Monitoring

**Check system health:**
```bash
curl "http://localhost:8000/api/v1/monitoring/system-health"
```

**Check device health:**
```bash
curl "http://localhost:8000/api/v1/monitoring/health/{device-id}"
```

## 🔄 Data Models

### Device Model
```json
{
  "id": "string",
  "name": "string",
  "device_type": "SDM120|PM2510-0D|XY-MD02|GENERIC",
  "host": "string",
  "port": 502,
  "unit_id": 1,
  "timeout": 3,
  "status": "CONNECTED|DISCONNECTED|ERROR",
  "metadata": {},
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Reading Model
```json
{
  "device_id": "string",
  "reading_type": "string",
  "value": 123.45,
  "unit": "V",
  "timestamp": "2024-01-01T00:00:00Z",
  "register_address": 4,
  "quality": "good"
}
```

### Health Check Model
```json
{
  "device_id": "string",
  "device_name": "string",
  "device_type": "SDM120",
  "status": "healthy|warning|error|disconnected",
  "connection_status": "connected|disconnected",
  "responsive": true,
  "has_recent_data": true,
  "last_reading": "2024-01-01T00:00:00Z",
  "last_check": "2024-01-01T00:00:00Z",
  "message": "Device is functioning normally"
}
```

## ⚡ Performance Tips

### Efficient Data Retrieval
- Use **pagination** for large datasets
- **Filter by date range** to limit results
- **Batch requests** when possible
- **Cache frequently accessed data**

### Optimal Request Patterns
```bash
# Good: Get specific device data
GET /api/v1/readings/latest/{device-id}

# Better: Get data with date range
GET /api/v1/readings?device_id={id}&start_time=2024-01-01T00:00:00Z

# Best: Use pagination for large datasets
GET /api/v1/readings?page=1&per_page=50
```

## 🔒 Security Best Practices

### Request Security
- **Validate input data** before sending requests
- **Use HTTPS** in production
- **Handle sensitive data** appropriately
- **Implement rate limiting** on client side

### Response Handling
- **Check response status codes**
- **Handle errors gracefully**
- **Validate response data**
- **Log security-relevant events**

## 📊 Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | OK | Request successful |
| `201` | Created | Resource created successfully |
| `400` | Bad Request | Invalid request data |
| `404` | Not Found | Resource not found |
| `422` | Validation Error | Request validation failed |
| `500` | Internal Error | Server error occurred |

## 🧪 Testing the API

### Using curl
```bash
# Test API health
curl http://localhost:8000/api/v1/health

# Test with JSON data
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}' \
     http://localhost:8000/api/v1/endpoint
```

### Using Python requests
```python
import requests

# GET request
response = requests.get('http://localhost:8000/api/v1/devices')
print(response.json())

# POST request
data = {
    "name": "Test Device",
    "device_type": "SDM120",
    "host": "10.1.2.1",
    "unit_id": 1
}
response = requests.post('http://localhost:8000/api/v1/devices', json=data)
print(response.json())
```

### Using JavaScript/Node.js
```javascript
// Using fetch API
const response = await fetch('http://localhost:8000/api/v1/devices');
const devices = await response.json();
console.log(devices);

// POST request
const newDevice = {
  name: "Test Device",
  device_type: "SDM120",
  host: "10.1.2.1",
  unit_id: 1
};

const response = await fetch('http://localhost:8000/api/v1/devices', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(newDevice)
});
```

## 🤝 API Versioning

### Current Version: v1
- Base path: `/api/v1/`
- Stable and backward compatible
- Regular updates with new features

### Future Versions
- New versions will be introduced as `/api/v2/`, etc.
- Previous versions will be supported for transition period
- Breaking changes will only occur in new versions

## 📞 Support

For API-related questions:

1. **Try the interactive Swagger UI** at `/docs`
2. **Check this documentation** for details
3. **Review example code** in the repository
4. **Search GitHub issues** for similar questions
5. **Open new issues** for bugs or feature requests

## 🔗 Related Documentation

- **[User Guide](../user-guide/)** - End-user documentation
- **[Developer Guide](../developer-guide/)** - Technical implementation
- **[Examples](../examples/)** - Practical usage examples
- **[Deployment](../deployment/)** - Production deployment guides

Ready to start using the API? Check out the **[API Overview](overview.md)** or jump straight to **[Quick Start](quick-start.md)**!