"""Device monitoring use cases."""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
import asyncio

from ...domain.entities import Device, Reading
from ...domain.repositories import DeviceRepository, ReadingRepository
from ...domain.value_objects import DeviceId
from ..interfaces import ModbusClient
from .data_collection import DataCollectionUseCase

logger = logging.getLogger(__name__)


class DeviceMonitoringUseCase:
    """Use cases for device monitoring and health checks."""
    
    def __init__(
        self,
        device_repository: DeviceRepository,
        reading_repository: ReadingRepository,
        data_collection_use_case: DataCollectionUseCase,
        modbus_client: ModbusClient
    ):
        self.device_repository = device_repository
        self.reading_repository = reading_repository
        self.data_collection_use_case = data_collection_use_case
        self.modbus_client = modbus_client
        self._monitoring_tasks = {}
    
    async def check_device_health(self, device_id: DeviceId) -> Dict[str, Any]:
        """Check health status of a device."""
        device = await self.device_repository.find_by_id(device_id)
        if not device:
            return {"status": "not_found", "message": "Device not found"}
        
        health_info = {
            "device_id": str(device_id),
            "device_name": device.name,
            "device_type": str(device.device_type),
            "connection_status": device.status.value,
            "last_check": datetime.utcnow().isoformat()
        }
        
        # Check connection
        try:
            if device.is_connected():
                is_responsive = await self._test_device_connection(device)
                health_info["responsive"] = is_responsive
                if not is_responsive:
                    health_info["status"] = "connection_error"
                    health_info["message"] = "Device not responding"
                else:
                    health_info["status"] = "healthy"
                    health_info["message"] = "Device is healthy"
            else:
                health_info["responsive"] = False
                health_info["status"] = "disconnected"
                health_info["message"] = "Device is disconnected"
        except Exception as e:
            health_info["responsive"] = False
            health_info["status"] = "error"
            health_info["message"] = f"Health check error: {str(e)}"
        
        # Check recent readings
        try:
            recent_readings = await self.reading_repository.find_by_device(
                device_id,
                start_time=datetime.utcnow() - timedelta(minutes=10),
                limit=1
            )
            
            health_info["has_recent_data"] = len(recent_readings) > 0
            if recent_readings:
                health_info["last_reading"] = recent_readings[0].timestamp.isoformat()
            
        except Exception as e:
            logger.error(f"Error checking recent readings for {device_id}: {e}")
            health_info["has_recent_data"] = False
        
        return health_info
    
    async def check_all_devices_health(self) -> List[Dict[str, Any]]:
        """Check health status of all devices."""
        devices = await self.device_repository.find_all()
        health_checks = []
        
        for device in devices:
            health_info = await self.check_device_health(device.id)
            health_checks.append(health_info)
        
        return health_checks
    
    async def start_monitoring(self, device_id: DeviceId, interval: int = 30) -> bool:
        """Start continuous monitoring of a device."""
        if device_id in self._monitoring_tasks:
            logger.warning(f"Monitoring already started for device: {device_id}")
            return False
        
        device = await self.device_repository.find_by_id(device_id)
        if not device:
            logger.error(f"Device not found for monitoring: {device_id}")
            return False
        
        task = asyncio.create_task(self._monitoring_loop(device_id, interval))
        self._monitoring_tasks[device_id] = task
        logger.info(f"Started monitoring for device: {device.name} (interval: {interval}s)")
        return True
    
    async def stop_monitoring(self, device_id: DeviceId) -> bool:
        """Stop monitoring of a device."""
        if device_id not in self._monitoring_tasks:
            return False
        
        task = self._monitoring_tasks.pop(device_id)
        task.cancel()
        
        try:
            await task
        except asyncio.CancelledError:
            pass
        
        device = await self.device_repository.find_by_id(device_id)
        device_name = device.name if device else str(device_id)
        logger.info(f"Stopped monitoring for device: {device_name}")
        return True
    
    async def stop_all_monitoring(self) -> None:
        """Stop monitoring for all devices."""
        device_ids = list(self._monitoring_tasks.keys())
        for device_id in device_ids:
            await self.stop_monitoring(device_id)
    
    async def get_monitoring_status(self) -> Dict[str, Any]:
        """Get status of all monitoring tasks."""
        status = {
            "total_monitored_devices": len(self._monitoring_tasks),
            "monitored_devices": [],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        for device_id in self._monitoring_tasks:
            device = await self.device_repository.find_by_id(device_id)
            status["monitored_devices"].append({
                "device_id": str(device_id),
                "device_name": device.name if device else "Unknown",
                "task_running": not self._monitoring_tasks[device_id].done()
            })
        
        return status
    
    async def _monitoring_loop(self, device_id: DeviceId, interval: int) -> None:
        """Continuous monitoring loop for a device."""
        while True:
            try:
                # Collect data
                readings = await self.data_collection_use_case.collect_device_data(device_id)
                
                # Check health
                health = await self.check_device_health(device_id)
                
                # Log monitoring info
                logger.debug(f"Monitoring {device_id}: {len(readings)} readings, status: {health.get('status')}")
                
                # Wait for next interval
                await asyncio.sleep(interval)
                
            except asyncio.CancelledError:
                logger.info(f"Monitoring cancelled for device: {device_id}")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop for {device_id}: {e}")
                await asyncio.sleep(interval)  # Continue monitoring even after errors
    
    async def _test_device_connection(self, device: Device) -> bool:
        """Test if device is responding."""
        try:
            # Try to read a single register to test connectivity
            result = await self.modbus_client.read_input_registers(0, 1)
            return result is not None
        except Exception as e:
            logger.debug(f"Device connection test failed for {device.name}: {e}")
            return False