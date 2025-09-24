"""Data collection use cases."""

from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

from ...domain.entities import Device, Reading, DeviceConfig, RegisterConfig
from ...domain.repositories import DeviceRepository, ReadingRepository, ConfigRepository
from ...domain.value_objects import DeviceId, ReadingType
from ..interfaces import ModbusClient

logger = logging.getLogger(__name__)


class DataCollectionUseCase:
    """Use cases for data collection from MODBUS devices."""
    
    def __init__(
        self,
        device_repository: DeviceRepository,
        reading_repository: ReadingRepository,
        config_repository: ConfigRepository,
        modbus_client: ModbusClient
    ):
        self.device_repository = device_repository
        self.reading_repository = reading_repository
        self.config_repository = config_repository
        self.modbus_client = modbus_client
    
    async def collect_device_data(self, device_id: DeviceId) -> List[Reading]:
        """Collect data from a specific device."""
        device = await self.device_repository.find_by_id(device_id)
        if not device:
            logger.error(f"Device not found: {device_id}")
            return []
        
        if not device.is_connected():
            logger.warning(f"Device not connected: {device.name}")
            return []
        
        config = await self.config_repository.find_config_by_id(device_id)
        if not config or not config.registers:
            logger.warning(f"No configuration found for device: {device.name}")
            return []
        
        readings = []
        timestamp = datetime.utcnow()
        
        for register_config in config.registers:
            try:
                value = await self._read_register_value(register_config)
                if value is not None:
                    # Apply scaling and offset
                    scaled_value = (value * register_config.scale_factor) + register_config.offset
                    
                    reading = Reading(
                        device_id=device_id,
                        reading_type=ReadingType(register_config.name),
                        value=scaled_value,
                        unit=register_config.unit,
                        timestamp=timestamp,
                        register_address=register_config.address,
                        quality="good"
                    )
                    readings.append(reading)
                else:
                    # Create reading with error quality
                    reading = Reading(
                        device_id=device_id,
                        reading_type=ReadingType(register_config.name),
                        value=0.0,
                        unit=register_config.unit,
                        timestamp=timestamp,
                        register_address=register_config.address,
                        quality="error"
                    )
                    readings.append(reading)
                    
            except Exception as e:
                logger.error(f"Error reading register {register_config.name}: {e}")
        
        # Save readings to repository
        if readings:
            await self.reading_repository.save_batch(readings)
            logger.info(f"Collected {len(readings)} readings from {device.name}")
        
        return readings
    
    async def collect_all_devices_data(self) -> Dict[DeviceId, List[Reading]]:
        """Collect data from all connected devices."""
        devices = await self.device_repository.find_connected()
        results = {}
        
        for device in devices:
            readings = await self.collect_device_data(device.id)
            results[device.id] = readings
        
        return results
    
    async def get_latest_readings(self, device_id: DeviceId) -> List[Reading]:
        """Get latest readings for a device."""
        return await self.reading_repository.find_latest_by_device(device_id)
    
    async def get_historical_readings(
        self,
        device_id: DeviceId,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Reading]:
        """Get historical readings for a device."""
        return await self.reading_repository.find_by_device(
            device_id, start_time, end_time, limit
        )
    
    async def _read_register_value(self, register_config: RegisterConfig) -> Optional[float]:
        """Read value from a register based on its configuration."""
        try:
            if register_config.data_type == "float32":
                return await self.modbus_client.read_float32(register_config.address)
            elif register_config.data_type == "uint16":
                value = await self.modbus_client.read_int16(register_config.address, signed=False)
                return float(value) if value is not None else None
            elif register_config.data_type == "int16":
                value = await self.modbus_client.read_int16(register_config.address, signed=True)
                return float(value) if value is not None else None
            elif register_config.data_type == "uint32":
                # Read two consecutive registers for 32-bit value
                registers = await self.modbus_client.read_input_registers(register_config.address, 2)
                if registers and len(registers) == 2:
                    # Combine registers (big-endian)
                    value = (registers[0] << 16) | registers[1]
                    return float(value)
                return None
            else:
                logger.warning(f"Unsupported data type: {register_config.data_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error reading register {register_config.address}: {e}")
            return None