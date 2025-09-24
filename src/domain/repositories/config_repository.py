"""Configuration repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities import DeviceConfig
from ..value_objects import DeviceId, DeviceType


class ConfigRepository(ABC):
    """Abstract configuration repository."""
    
    @abstractmethod
    async def save_config(self, config: DeviceConfig) -> None:
        """Save device configuration."""
        pass
    
    @abstractmethod
    async def find_config_by_id(self, device_id: DeviceId) -> Optional[DeviceConfig]:
        """Find configuration by device ID."""
        pass
    
    @abstractmethod
    async def find_configs_by_type(self, device_type: DeviceType) -> List[DeviceConfig]:
        """Find configurations by device type."""
        pass
    
    @abstractmethod
    async def find_all_configs(self) -> List[DeviceConfig]:
        """Find all device configurations."""
        pass
    
    @abstractmethod
    async def delete_config(self, device_id: DeviceId) -> bool:
        """Delete device configuration."""
        pass