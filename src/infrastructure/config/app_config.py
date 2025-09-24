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
class AppConfig:
    """Application configuration."""
    
    # Basic settings
    debug: bool = False
    environment: str = "development"
    
    # Component configurations
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    modbus: ModbusConfig = field(default_factory=ModbusConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    
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
    
    # Remove empty values
    env_overrides = {k: v for k, v in env_overrides.items() if v}
    
    # Merge configurations (env overrides file overrides defaults)
    config_data.update(env_overrides)
    
    return AppConfig.from_dict(config_data)