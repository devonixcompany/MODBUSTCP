# Legacy Scripts

These are the original individual MODBUS device scripts that have been replaced by the new clean architecture implementation.

## Replaced Scripts

- `sdm120_read.py` → Use `modbustcp device add --type SDM120` + `modbustcp data collect`
- `pm2510_0d_summary.py` → Use `modbustcp device add --type PM2510-0D` + `modbustcp data collect`
- `xy_md02_summary.py` → Use `modbustcp device add --type XY-MD02` + `modbustcp data collect`

## Migration

The new architecture provides the same functionality with improved:
- Error handling and logging
- Configuration management  
- Monitoring and health checks
- Production readiness
- Docker support

## Usage with New System

1. Add device:
```bash
modbustcp device add --name "Energy Meter" --type SDM120 --host 10.1.2.1 --unit 1
```

2. Collect data:
```bash
modbustcp data collect <device-id>
```

3. Monitor device:
```bash
modbustcp monitor health <device-id>
```

See main README.md for complete documentation.
