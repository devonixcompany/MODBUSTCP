"""Reading repository interface."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from ..entities import Reading
from ..value_objects import DeviceId, ReadingType


class ReadingRepository(ABC):
    """Abstract reading repository."""
    
    @abstractmethod
    async def save(self, reading: Reading) -> None:
        """Save a reading."""
        pass
    
    @abstractmethod
    async def save_batch(self, readings: List[Reading]) -> None:
        """Save multiple readings."""
        pass
    
    @abstractmethod
    async def find_by_device(
        self, 
        device_id: DeviceId, 
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Reading]:
        """Find readings by device."""
        pass
    
    @abstractmethod
    async def find_by_type(
        self, 
        reading_type: ReadingType,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Reading]:
        """Find readings by type."""
        pass
    
    @abstractmethod
    async def find_latest_by_device(self, device_id: DeviceId) -> List[Reading]:
        """Find latest readings for a device."""
        pass
    
    @abstractmethod
    async def delete_old_readings(self, older_than: datetime) -> int:
        """Delete old readings and return count of deleted records."""
        pass