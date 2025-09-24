"""Reading entity for device measurements."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, Union

from ..value_objects import DeviceId, ReadingType


@dataclass
class Reading:
    """Device reading entity."""
    
    device_id: DeviceId
    reading_type: ReadingType
    value: Union[float, int]
    unit: str
    timestamp: datetime
    register_address: int
    quality: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate reading data after initialization."""
        if not isinstance(self.value, (int, float)):
            raise ValueError("Reading value must be numeric")
        
        if not self.unit.strip():
            raise ValueError("Unit cannot be empty")
        
        if self.register_address < 0:
            raise ValueError("Register address must be non-negative")
    
    def is_valid(self) -> bool:
        """Check if reading is valid."""
        return (
            self.value is not None and
            isinstance(self.value, (int, float)) and
            not (isinstance(self.value, float) and 
                 (self.value != self.value or  # NaN check
                  self.value == float('inf') or 
                  self.value == float('-inf')))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert reading to dictionary."""
        return {
            "device_id": str(self.device_id),
            "reading_type": str(self.reading_type),
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
            "register_address": self.register_address,
            "quality": self.quality,
            "metadata": self.metadata or {}
        }