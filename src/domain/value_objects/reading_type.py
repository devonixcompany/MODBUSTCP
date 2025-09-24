"""Reading type value object."""

from dataclasses import dataclass
from enum import Enum


class CommonReadingType(Enum):
    """Common reading types for MODBUS devices."""
    
    # Energy meter readings (SDM120)
    VOLTAGE = "voltage"
    CURRENT = "current"
    ACTIVE_POWER = "active_power"
    APPARENT_POWER = "apparent_power"
    REACTIVE_POWER = "reactive_power"
    POWER_FACTOR = "power_factor"
    FREQUENCY = "frequency"
    TOTAL_ENERGY = "total_energy"
    
    # Environmental readings
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PM25 = "pm25"
    PM10 = "pm10"
    
    # Generic
    GENERIC = "generic"


@dataclass(frozen=True)
class ReadingType:
    """Reading type value object."""
    
    value: str
    
    def __post_init__(self):
        """Validate reading type."""
        if not self.value or not self.value.strip():
            raise ValueError("Reading type cannot be empty")
        
        # Normalize the value
        object.__setattr__(self, 'value', self.value.strip().lower())
    
    @classmethod
    def voltage(cls) -> 'ReadingType':
        """Create voltage reading type."""
        return cls(CommonReadingType.VOLTAGE.value)
    
    @classmethod
    def current(cls) -> 'ReadingType':
        """Create current reading type."""
        return cls(CommonReadingType.CURRENT.value)
    
    @classmethod
    def active_power(cls) -> 'ReadingType':
        """Create active power reading type."""
        return cls(CommonReadingType.ACTIVE_POWER.value)
    
    @classmethod
    def temperature(cls) -> 'ReadingType':
        """Create temperature reading type."""
        return cls(CommonReadingType.TEMPERATURE.value)
    
    @classmethod
    def humidity(cls) -> 'ReadingType':
        """Create humidity reading type."""
        return cls(CommonReadingType.HUMIDITY.value)
    
    @classmethod
    def pm25(cls) -> 'ReadingType':
        """Create PM2.5 reading type."""
        return cls(CommonReadingType.PM25.value)
    
    @classmethod
    def pm10(cls) -> 'ReadingType':
        """Create PM10 reading type."""
        return cls(CommonReadingType.PM10.value)
    
    def is_environmental(self) -> bool:
        """Check if reading type is environmental."""
        environmental_types = {
            CommonReadingType.TEMPERATURE.value,
            CommonReadingType.HUMIDITY.value,
            CommonReadingType.PM25.value,
            CommonReadingType.PM10.value,
        }
        return self.value in environmental_types
    
    def is_electrical(self) -> bool:
        """Check if reading type is electrical."""
        electrical_types = {
            CommonReadingType.VOLTAGE.value,
            CommonReadingType.CURRENT.value,
            CommonReadingType.ACTIVE_POWER.value,
            CommonReadingType.APPARENT_POWER.value,
            CommonReadingType.REACTIVE_POWER.value,
            CommonReadingType.POWER_FACTOR.value,
            CommonReadingType.FREQUENCY.value,
            CommonReadingType.TOTAL_ENERGY.value,
        }
        return self.value in electrical_types
    
    def __str__(self) -> str:
        """String representation."""
        return self.value
    
    def __repr__(self) -> str:
        """Representation for debugging."""
        return f"ReadingType('{self.value}')"