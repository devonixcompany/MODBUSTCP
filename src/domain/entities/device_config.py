"""Device configuration entity."""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from ..value_objects import DeviceId, DeviceType, ModbusAddress


@dataclass
class RegisterConfig:
    """Configuration for a MODBUS register."""
    
    name: str
    address: int
    data_type: str  # 'float32', 'uint16', 'int16', etc.
    unit: str
    scale_factor: float = 1.0
    offset: float = 0.0
    description: Optional[str] = None


@dataclass
class DeviceConfig:
    """Configuration for a MODBUS device."""
    
    id: DeviceId
    name: str
    device_type: DeviceType
    address: ModbusAddress
    unit_id: int
    timeout: int = 3
    registers: List[RegisterConfig] = None
    polling_interval: int = 5  # seconds
    retry_count: int = 3
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.registers is None:
            self.registers = []
    
    def add_register(self, register: RegisterConfig) -> None:
        """Add a register configuration."""
        self.registers.append(register)
    
    def get_register_by_name(self, name: str) -> Optional[RegisterConfig]:
        """Get register configuration by name."""
        for register in self.registers:
            if register.name == name:
                return register
        return None
    
    def get_register_addresses(self) -> List[int]:
        """Get all register addresses."""
        return [reg.address for reg in self.registers]