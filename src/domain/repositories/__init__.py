"""Domain repository interfaces."""

from .device_repository import DeviceRepository
from .reading_repository import ReadingRepository
from .config_repository import ConfigRepository

__all__ = ["DeviceRepository", "ReadingRepository", "ConfigRepository"]