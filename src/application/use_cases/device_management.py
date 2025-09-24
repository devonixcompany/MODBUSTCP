"""Device management use cases."""

from typing import List, Optional
import logging

from ...domain.entities import Device, DeviceConfig
from ...domain.repositories import DeviceRepository, ConfigRepository
from ...domain.value_objects import DeviceId, DeviceType, ModbusAddress
from ..interfaces import ModbusClient

logger = logging.getLogger(__name__)


class DeviceManagementUseCase:
    """Use cases for device management."""
    
    def __init__(
        self,
        device_repository: DeviceRepository,
        config_repository: ConfigRepository,
        modbus_client: ModbusClient
    ):
        self.device_repository = device_repository
        self.config_repository = config_repository
        self.modbus_client = modbus_client
    
    async def add_device(
        self,
        name: str,
        device_type: DeviceType,
        address: ModbusAddress,
        unit_id: int,
        device_id: Optional[DeviceId] = None
    ) -> Device:
        """Add a new device."""
        if device_id is None:
            device_id = DeviceId.generate()
        
        device = Device(
            id=device_id,
            name=name,
            device_type=device_type,
            address=address,
            unit_id=unit_id
        )
        
        await self.device_repository.save(device)
        logger.info(f"Added device: {name} ({device_type}) at {address}")
        return device
    
    async def remove_device(self, device_id: DeviceId) -> bool:
        """Remove a device."""
        # First disconnect if connected
        device = await self.device_repository.find_by_id(device_id)
        if device and device.is_connected():
            await self.disconnect_device(device_id)
        
        # Remove device and its configuration
        device_deleted = await self.device_repository.delete(device_id)
        config_deleted = await self.config_repository.delete_config(device_id)
        
        if device_deleted:
            logger.info(f"Removed device: {device_id}")
        
        return device_deleted
    
    async def get_device(self, device_id: DeviceId) -> Optional[Device]:
        """Get device by ID."""
        return await self.device_repository.find_by_id(device_id)
    
    async def list_devices(self) -> List[Device]:
        """List all devices."""
        return await self.device_repository.find_all()
    
    async def connect_device(self, device_id: DeviceId, timeout: int = 3) -> bool:
        """Connect to a device."""
        device = await self.device_repository.find_by_id(device_id)
        if not device:
            logger.error(f"Device not found: {device_id}")
            return False
        
        try:
            success = await self.modbus_client.connect(
                device.address, device.unit_id, timeout
            )
            
            if success:
                device.connect()
                await self.device_repository.save(device)
                logger.info(f"Connected to device: {device.name}")
            else:
                device.set_error()
                await self.device_repository.save(device)
                logger.error(f"Failed to connect to device: {device.name}")
            
            return success
            
        except Exception as e:
            device.set_error()
            await self.device_repository.save(device)
            logger.error(f"Error connecting to device {device.name}: {e}")
            return False
    
    async def disconnect_device(self, device_id: DeviceId) -> bool:
        """Disconnect from a device."""
        device = await self.device_repository.find_by_id(device_id)
        if not device:
            return False
        
        try:
            await self.modbus_client.disconnect()
            device.disconnect()
            await self.device_repository.save(device)
            logger.info(f"Disconnected from device: {device.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error disconnecting from device {device.name}: {e}")
            return False
    
    async def update_device_config(self, config: DeviceConfig) -> None:
        """Update device configuration."""
        await self.config_repository.save_config(config)
        logger.info(f"Updated configuration for device: {config.id}")
    
    async def get_device_config(self, device_id: DeviceId) -> Optional[DeviceConfig]:
        """Get device configuration."""
        return await self.config_repository.find_config_by_id(device_id)