"""In-memory repository implementations."""

from datetime import datetime
from typing import List, Optional, Dict
import asyncio

from ...domain.entities import Device, Reading, DeviceConfig
from ...domain.repositories import DeviceRepository, ReadingRepository, ConfigRepository
from ...domain.value_objects import DeviceId, DeviceType, ReadingType


class InMemoryDeviceRepository(DeviceRepository):
    """In-memory device repository implementation."""
    
    def __init__(self):
        self._devices: Dict[str, Device] = {}
        self._lock = asyncio.Lock()
    
    async def save(self, device: Device) -> None:
        """Save a device."""
        async with self._lock:
            self._devices[str(device.id)] = device
    
    async def find_by_id(self, device_id: DeviceId) -> Optional[Device]:
        """Find device by ID."""
        async with self._lock:
            return self._devices.get(str(device_id))
    
    async def find_all(self) -> List[Device]:
        """Find all devices."""
        async with self._lock:
            return list(self._devices.values())
    
    async def delete(self, device_id: DeviceId) -> bool:
        """Delete a device."""
        async with self._lock:
            return self._devices.pop(str(device_id), None) is not None
    
    async def find_connected(self) -> List[Device]:
        """Find all connected devices."""
        async with self._lock:
            return [device for device in self._devices.values() if device.is_connected()]


class InMemoryReadingRepository(ReadingRepository):
    """In-memory reading repository implementation."""
    
    def __init__(self):
        self._readings: List[Reading] = []
        self._lock = asyncio.Lock()
    
    async def save(self, reading: Reading) -> None:
        """Save a reading."""
        async with self._lock:
            self._readings.append(reading)
    
    async def save_batch(self, readings: List[Reading]) -> None:
        """Save multiple readings."""
        async with self._lock:
            self._readings.extend(readings)
    
    async def find_by_device(
        self, 
        device_id: DeviceId, 
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Reading]:
        """Find readings by device."""
        async with self._lock:
            filtered_readings = [
                reading for reading in self._readings 
                if reading.device_id == device_id
            ]
            
            # Apply time filters
            if start_time:
                filtered_readings = [
                    reading for reading in filtered_readings 
                    if reading.timestamp >= start_time
                ]
            
            if end_time:
                filtered_readings = [
                    reading for reading in filtered_readings 
                    if reading.timestamp <= end_time
                ]
            
            # Sort by timestamp (most recent first)
            filtered_readings.sort(key=lambda r: r.timestamp, reverse=True)
            
            # Apply limit
            if limit:
                filtered_readings = filtered_readings[:limit]
            
            return filtered_readings
    
    async def find_by_type(
        self, 
        reading_type: ReadingType,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Reading]:
        """Find readings by type."""
        async with self._lock:
            filtered_readings = [
                reading for reading in self._readings 
                if reading.reading_type == reading_type
            ]
            
            # Apply time filters
            if start_time:
                filtered_readings = [
                    reading for reading in filtered_readings 
                    if reading.timestamp >= start_time
                ]
            
            if end_time:
                filtered_readings = [
                    reading for reading in filtered_readings 
                    if reading.timestamp <= end_time
                ]
            
            # Sort by timestamp (most recent first)
            filtered_readings.sort(key=lambda r: r.timestamp, reverse=True)
            
            # Apply limit
            if limit:
                filtered_readings = filtered_readings[:limit]
            
            return filtered_readings
    
    async def find_latest_by_device(self, device_id: DeviceId) -> List[Reading]:
        """Find latest readings for a device."""
        async with self._lock:
            device_readings = [
                reading for reading in self._readings 
                if reading.device_id == device_id
            ]
            
            if not device_readings:
                return []
            
            # Group by reading type and get latest for each
            latest_readings = {}
            for reading in device_readings:
                reading_type = str(reading.reading_type)
                if (reading_type not in latest_readings or 
                    reading.timestamp > latest_readings[reading_type].timestamp):
                    latest_readings[reading_type] = reading
            
            return list(latest_readings.values())
    
    async def delete_old_readings(self, older_than: datetime) -> int:
        """Delete old readings and return count of deleted records."""
        async with self._lock:
            old_readings = [
                reading for reading in self._readings 
                if reading.timestamp < older_than
            ]
            
            count = len(old_readings)
            self._readings = [
                reading for reading in self._readings 
                if reading.timestamp >= older_than
            ]
            
            return count


class InMemoryConfigRepository(ConfigRepository):
    """In-memory configuration repository implementation."""
    
    def __init__(self):
        self._configs: Dict[str, DeviceConfig] = {}
        self._lock = asyncio.Lock()
    
    async def save_config(self, config: DeviceConfig) -> None:
        """Save device configuration."""
        async with self._lock:
            self._configs[str(config.id)] = config
    
    async def find_config_by_id(self, device_id: DeviceId) -> Optional[DeviceConfig]:
        """Find configuration by device ID."""
        async with self._lock:
            return self._configs.get(str(device_id))
    
    async def find_configs_by_type(self, device_type: DeviceType) -> List[DeviceConfig]:
        """Find configurations by device type."""
        async with self._lock:
            return [
                config for config in self._configs.values() 
                if config.device_type == device_type
            ]
    
    async def find_all_configs(self) -> List[DeviceConfig]:
        """Find all device configurations."""
        async with self._lock:
            return list(self._configs.values())
    
    async def delete_config(self, device_id: DeviceId) -> bool:
        """Delete device configuration."""
        async with self._lock:
            return self._configs.pop(str(device_id), None) is not None