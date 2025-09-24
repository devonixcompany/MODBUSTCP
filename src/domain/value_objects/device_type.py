"""Device type value object."""

from dataclasses import dataclass
from enum import Enum


class SupportedDeviceType(Enum):
    """Supported MODBUS device types."""
    
    SDM120 = "SDM120"  # Energy meter
    PM2510_0D = "PM2510-0D"  # Dust sensor
    XY_MD02 = "XY-MD02"  # Temperature/Humidity sensor
    GENERIC = "GENERIC"  # Generic MODBUS device


@dataclass(frozen=True)
class DeviceType:
    """Device type value object."""
    
    value: str
    
    def __post_init__(self):
        """Validate device type."""
        if not self.value or not self.value.strip():
            raise ValueError("Device type cannot be empty")
        
        # Normalize the value
        object.__setattr__(self, 'value', self.value.strip().upper())
    
    @classmethod
    def sdm120(cls) -> 'DeviceType':
        """Create SDM120 device type."""
        return cls(SupportedDeviceType.SDM120.value)
    
    @classmethod
    def pm2510_0d(cls) -> 'DeviceType':
        """Create PM2510-0D device type."""
        return cls(SupportedDeviceType.PM2510_0D.value)
    
    @classmethod
    def xy_md02(cls) -> 'DeviceType':
        """Create XY-MD02 device type."""
        return cls(SupportedDeviceType.XY_MD02.value)
    
    @classmethod
    def generic(cls) -> 'DeviceType':
        """Create generic device type."""
        return cls(SupportedDeviceType.GENERIC.value)
    
    def is_supported(self) -> bool:
        """Check if device type is supported."""
        try:
            SupportedDeviceType(self.value)
            return True
        except ValueError:
            return False
    
    def __str__(self) -> str:
        """String representation."""
        return self.value
    
    def __repr__(self) -> str:
        """Representation for debugging."""
        return f"DeviceType('{self.value}')"