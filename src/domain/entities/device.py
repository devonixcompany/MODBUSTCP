"""Device entity for MODBUS devices."""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum

from ..value_objects import DeviceId, DeviceType, ModbusAddress


class DeviceStatus(Enum):
    """Device connection status."""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


@dataclass
class Device:
    """MODBUS device entity."""
    
    id: DeviceId
    name: str
    device_type: DeviceType
    address: ModbusAddress
    unit_id: int
    status: DeviceStatus = DeviceStatus.DISCONNECTED
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate device data after initialization."""
        if not self.name.strip():
            raise ValueError("Device name cannot be empty")
        
        if self.unit_id < 1 or self.unit_id > 247:
            raise ValueError("Unit ID must be between 1 and 247")
    
    def connect(self) -> None:
        """Mark device as connected."""
        self.status = DeviceStatus.CONNECTED
    
    def disconnect(self) -> None:
        """Mark device as disconnected."""
        self.status = DeviceStatus.DISCONNECTED
    
    def set_error(self) -> None:
        """Mark device as in error state."""
        self.status = DeviceStatus.ERROR
    
    def is_connected(self) -> bool:
        """Check if device is connected."""
        return self.status == DeviceStatus.CONNECTED