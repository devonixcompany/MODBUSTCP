"""Device ID value object."""

from dataclasses import dataclass
import uuid
from typing import Union


@dataclass(frozen=True)
class DeviceId:
    """Unique identifier for a device."""
    
    value: str
    
    def __post_init__(self):
        """Validate device ID."""
        if not self.value or not self.value.strip():
            raise ValueError("Device ID cannot be empty")
        
        # Ensure it's a string
        object.__setattr__(self, 'value', str(self.value).strip())
    
    @classmethod
    def generate(cls) -> 'DeviceId':
        """Generate a new unique device ID."""
        return cls(str(uuid.uuid4()))
    
    @classmethod
    def from_string(cls, value: str) -> 'DeviceId':
        """Create device ID from string."""
        return cls(value)
    
    def __str__(self) -> str:
        """String representation."""
        return self.value
    
    def __repr__(self) -> str:
        """Representation for debugging."""
        return f"DeviceId('{self.value}')"