"""Device repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities import Device
from ..value_objects import DeviceId


class DeviceRepository(ABC):
    """Abstract device repository."""
    
    @abstractmethod
    async def save(self, device: Device) -> None:
        """Save a device."""
        pass
    
    @abstractmethod
    async def find_by_id(self, device_id: DeviceId) -> Optional[Device]:
        """Find device by ID."""
        pass
    
    @abstractmethod
    async def find_all(self) -> List[Device]:
        """Find all devices."""
        pass
    
    @abstractmethod
    async def delete(self, device_id: DeviceId) -> bool:
        """Delete a device."""
        pass
    
    @abstractmethod
    async def find_connected(self) -> List[Device]:
        """Find all connected devices."""
        pass