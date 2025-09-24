"""Application configuration management."""

import os
import yaml
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None


@dataclass
class ModbusConfig:
    """MODBUS configuration."""
    default_timeout: int = 3
    default_retry_count: int = 3
    connection_pool_size: int = 10


@dataclass
class MonitoringConfig:
    """Monitoring configuration."""
    default_poll_interval: int = 30
    health_check_interval: int = 60
    max_reading_age_hours: int = 24
    

@dataclass
class DatabaseConfig:
    """Database configuration."""
    connection_string: str = "postgresql://user:password@localhost:5432/modbustcp"
    reading_store: str = "postgresql"  # postgresql or influxdb
    pool_size: int = 10
    max_overflow: int = 20
    echo: bool = False


@dataclass
class InfluxDBConfig:
    """InfluxDB configuration."""
    url: str = "http://localhost:8086"
    token: str = ""
    org: str = "modbustcp"
    bucket: str = "readings"


@dataclass
class APIConfig:
    """API configuration."""
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    reload: bool = False
    cors_origins: list = field(default_factory=lambda: ["*"])


@dataclass
class AppConfig:
    """Application configuration."""
    
    # Basic settings
    debug: bool = False
    environment: str = "development"
    
    # Component configurations
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    modbus: ModbusConfig = field(default_factory=ModbusConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    influxdb: InfluxDBConfig = field(default_factory=InfluxDBConfig)
    api: APIConfig = field(default_factory=APIConfig)
    
    # Device configurations
    devices: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppConfig':
        """Create configuration from dictionary."""
        config = cls()
        
        # Basic settings
        config.debug = data.get('debug', False)
        config.environment = data.get('environment', 'development')
        
        # Logging configuration
        if 'logging' in data:
            log_data = data['logging']
            config.logging = LoggingConfig(
                level=log_data.get('level', 'INFO'),
                format=log_data.get('format', config.logging.format),
                file=log_data.get('file')
            )
        
        # MODBUS configuration
        if 'modbus' in data:
            modbus_data = data['modbus']
            config.modbus = ModbusConfig(
                default_timeout=modbus_data.get('default_timeout', 3),
                default_retry_count=modbus_data.get('default_retry_count', 3),
                connection_pool_size=modbus_data.get('connection_pool_size', 10)
            )
        
        # Monitoring configuration
        if 'monitoring' in data:
            monitor_data = data['monitoring']
            config.monitoring = MonitoringConfig(
                default_poll_interval=monitor_data.get('default_poll_interval', 30),
                health_check_interval=monitor_data.get('health_check_interval', 60),
                max_reading_age_hours=monitor_data.get('max_reading_age_hours', 24)
            )
        
        # Database configuration
        if 'database' in data:
            db_data = data['database']
            config.database = DatabaseConfig(
                connection_string=db_data.get('connection_string', config.database.connection_string),
                reading_store=db_data.get('reading_store', 'postgresql'),
                pool_size=db_data.get('pool_size', 10),
                max_overflow=db_data.get('max_overflow', 20),
                echo=db_data.get('echo', False)
            )
        
        # InfluxDB configuration
        if 'influxdb' in data:
            influx_data = data['influxdb']
            config.influxdb = InfluxDBConfig(
                url=influx_data.get('url', 'http://localhost:8086'),
                token=influx_data.get('token', ''),
                org=influx_data.get('org', 'modbustcp'),
                bucket=influx_data.get('bucket', 'readings')
            )
        
        # API configuration
        if 'api' in data:
            api_data = data['api']
            config.api = APIConfig(
                host=api_data.get('host', '0.0.0.0'),
                port=api_data.get('port', 8000),
                workers=api_data.get('workers', 1),
                reload=api_data.get('reload', False),
                cors_origins=api_data.get('cors_origins', ['*'])
            )
        
        # Device configurations
        config.devices = data.get('devices', {})
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'debug': self.debug,
            'environment': self.environment,
            'logging': {
                'level': self.logging.level,
                'format': self.logging.format,
                'file': self.logging.file
            },
            'modbus': {
                'default_timeout': self.modbus.default_timeout,
                'default_retry_count': self.modbus.default_retry_count,
                'connection_pool_size': self.modbus.connection_pool_size
            },
            'monitoring': {
                'default_poll_interval': self.monitoring.default_poll_interval,
                'health_check_interval': self.monitoring.health_check_interval,
                'max_reading_age_hours': self.monitoring.max_reading_age_hours
            },
            'database': {
                'connection_string': self.database.connection_string,
                'reading_store': self.database.reading_store,
                'pool_size': self.database.pool_size,
                'max_overflow': self.database.max_overflow,
                'echo': self.database.echo
            },
            'influxdb': {
                'url': self.influxdb.url,
                'token': self.influxdb.token,
                'org': self.influxdb.org,
                'bucket': self.influxdb.bucket
            },
            'api': {
                'host': self.api.host,
                'port': self.api.port,
                'workers': self.api.workers,
                'reload': self.api.reload,
                'cors_origins': self.api.cors_origins
            },
            'devices': self.devices
        }


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """Load application configuration from file or environment."""
    
    # Default configuration
    config_data = {}
    
    # Try to load from file
    if config_path:
        config_file = Path(config_path)
    else:
        # Look for config file in standard locations
        possible_paths = [
            Path("config.yaml"),
            Path("config.yml"),
            Path("config/config.yaml"),
            Path("config/config.yml"),
            Path("/etc/modbustcp/config.yaml"),
        ]
        
        config_file = None
        for path in possible_paths:
            if path.exists():
                config_file = path
                break
    
    if config_file and config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    # Override with environment variables
    env_overrides = {
        'debug': os.getenv('MODBUS_DEBUG', '').lower() in ('true', '1', 'yes'),
        'environment': os.getenv('MODBUS_ENVIRONMENT', 'development'),
    }
    
    # Database environment variables
    if 'database' not in config_data:
        config_data['database'] = {}
    
    if os.getenv('DATABASE_URL'):
        config_data['database']['connection_string'] = os.getenv('DATABASE_URL')
    
    if os.getenv('READING_STORE'):
        config_data['database']['reading_store'] = os.getenv('READING_STORE')
    
    # InfluxDB environment variables
    if 'influxdb' not in config_data:
        config_data['influxdb'] = {}
    
    if os.getenv('INFLUXDB_URL'):
        config_data['influxdb']['url'] = os.getenv('INFLUXDB_URL')
    if os.getenv('INFLUXDB_TOKEN'):
        config_data['influxdb']['token'] = os.getenv('INFLUXDB_TOKEN')
    if os.getenv('INFLUXDB_ORG'):
        config_data['influxdb']['org'] = os.getenv('INFLUXDB_ORG')
    if os.getenv('INFLUXDB_BUCKET'):
        config_data['influxdb']['bucket'] = os.getenv('INFLUXDB_BUCKET')
    
    # API environment variables
    if 'api' not in config_data:
        config_data['api'] = {}
    
    if os.getenv('API_HOST'):
        config_data['api']['host'] = os.getenv('API_HOST')
    if os.getenv('API_PORT'):
        config_data['api']['port'] = int(os.getenv('API_PORT'))
    
    # Remove empty values
    env_overrides = {k: v for k, v in env_overrides.items() if v}
    
    # Merge configurations (env overrides file overrides defaults)
    config_data.update(env_overrides)
    
    return AppConfig.from_dict(config_data)