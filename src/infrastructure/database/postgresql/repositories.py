"""PostgreSQL repository implementations."""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from domain.entities import Device, Reading, DeviceConfig, RegisterConfig
from domain.repositories import DeviceRepository, ReadingRepository, ConfigRepository
from domain.value_objects import DeviceId, DeviceType, ModbusAddress, ReadingType
from ..models import Base, DeviceModel, ReadingModel, DeviceConfigModel


class PostgreSQLDeviceRepository(DeviceRepository):
    """PostgreSQL implementation of device repository."""
    
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=self.engine)
    
    def _model_to_entity(self, model: DeviceModel) -> Device:
        """Convert database model to domain entity."""
        return Device(
            id=DeviceId(model.id),
            name=model.name,
            device_type=DeviceType(model.device_type),
            address=ModbusAddress(model.host, model.port),
            unit_id=model.unit_id,
            status=model.status,
            metadata=model.metadata
        )
    
    def _entity_to_model(self, entity: Device) -> DeviceModel:
        """Convert domain entity to database model."""
        return DeviceModel(
            id=str(entity.id),
            name=entity.name,
            device_type=str(entity.device_type),
            host=entity.address.host,
            port=entity.address.port,
            unit_id=entity.unit_id,
            status=entity.status,
            metadata=entity.metadata
        )
    
    async def save(self, device: Device) -> None:
        """Save a device."""
        with self.SessionLocal() as session:
            try:
                # Check if device exists
                existing = session.get(DeviceModel, str(device.id))
                if existing:
                    # Update existing device
                    existing.name = device.name
                    existing.device_type = str(device.device_type)
                    existing.host = device.address.host
                    existing.port = device.address.port
                    existing.unit_id = device.unit_id
                    existing.status = device.status
                    existing.metadata = device.metadata
                else:
                    # Create new device
                    model = self._entity_to_model(device)
                    session.add(model)
                
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Failed to save device: {e}")
    
    async def find_by_id(self, device_id: DeviceId) -> Optional[Device]:
        """Find device by ID."""
        with self.SessionLocal() as session:
            model = session.get(DeviceModel, str(device_id))
            return self._model_to_entity(model) if model else None
    
    async def find_all(self) -> List[Device]:
        """Find all devices."""
        with self.SessionLocal() as session:
            models = session.execute(select(DeviceModel)).scalars().all()
            return [self._model_to_entity(model) for model in models]
    
    async def delete(self, device_id: DeviceId) -> bool:
        """Delete a device."""
        with self.SessionLocal() as session:
            model = session.get(DeviceModel, str(device_id))
            if model:
                session.delete(model)
                session.commit()
                return True
            return False
    
    async def find_connected(self) -> List[Device]:
        """Find all connected devices."""
        with self.SessionLocal() as session:
            stmt = select(DeviceModel).where(DeviceModel.status == "CONNECTED")
            models = session.execute(stmt).scalars().all()
            return [self._model_to_entity(model) for model in models]


class PostgreSQLReadingRepository(ReadingRepository):
    """PostgreSQL implementation of reading repository."""
    
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=self.engine)
    
    def _model_to_entity(self, model: ReadingModel) -> Reading:
        """Convert database model to domain entity."""
        return Reading(
            device_id=DeviceId(model.device_id),
            reading_type=ReadingType(model.reading_type),
            value=model.value,
            unit=model.unit,
            timestamp=model.timestamp,
            register_address=model.register_address,
            quality=model.quality,
            metadata=model.metadata
        )
    
    def _entity_to_model(self, entity: Reading) -> ReadingModel:
        """Convert domain entity to database model."""
        return ReadingModel(
            device_id=str(entity.device_id),
            reading_type=str(entity.reading_type),
            value=entity.value,
            unit=entity.unit,
            timestamp=entity.timestamp,
            register_address=entity.register_address,
            quality=entity.quality,
            metadata=entity.metadata
        )
    
    async def save(self, reading: Reading) -> None:
        """Save a reading."""
        with self.SessionLocal() as session:
            model = self._entity_to_model(reading)
            session.add(model)
            session.commit()
    
    async def save_batch(self, readings: List[Reading]) -> None:
        """Save multiple readings."""
        with self.SessionLocal() as session:
            models = [self._entity_to_model(reading) for reading in readings]
            session.add_all(models)
            session.commit()
    
    async def find_by_device(
        self,
        device_id: DeviceId,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Reading]:
        """Find readings by device."""
        with self.SessionLocal() as session:
            stmt = select(ReadingModel).where(ReadingModel.device_id == str(device_id))
            
            if start_time:
                stmt = stmt.where(ReadingModel.timestamp >= start_time)
            if end_time:
                stmt = stmt.where(ReadingModel.timestamp <= end_time)
            
            stmt = stmt.order_by(desc(ReadingModel.timestamp))
            
            if limit:
                stmt = stmt.limit(limit)
            
            models = session.execute(stmt).scalars().all()
            return [self._model_to_entity(model) for model in models]
    
    async def find_by_type(
        self,
        reading_type: ReadingType,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Reading]:
        """Find readings by type."""
        with self.SessionLocal() as session:
            stmt = select(ReadingModel).where(ReadingModel.reading_type == str(reading_type))
            
            if start_time:
                stmt = stmt.where(ReadingModel.timestamp >= start_time)
            if end_time:
                stmt = stmt.where(ReadingModel.timestamp <= end_time)
            
            stmt = stmt.order_by(desc(ReadingModel.timestamp))
            
            if limit:
                stmt = stmt.limit(limit)
            
            models = session.execute(stmt).scalars().all()
            return [self._model_to_entity(model) for model in models]
    
    async def find_latest_by_device(self, device_id: DeviceId) -> List[Reading]:
        """Find latest readings for a device."""
        with self.SessionLocal() as session:
            # Use a window function to get the latest reading for each type
            from sqlalchemy import text
            
            sql = text("""
                SELECT * FROM (
                    SELECT *,
                           ROW_NUMBER() OVER (
                               PARTITION BY reading_type 
                               ORDER BY timestamp DESC
                           ) as rn
                    FROM readings
                    WHERE device_id = :device_id
                ) ranked
                WHERE rn = 1
                ORDER BY timestamp DESC
            """)
            
            result = session.execute(sql, {"device_id": str(device_id)})
            
            readings = []
            for row in result:
                reading = Reading(
                    device_id=DeviceId(row.device_id),
                    reading_type=ReadingType(row.reading_type),
                    value=row.value,
                    unit=row.unit,
                    timestamp=row.timestamp,
                    register_address=row.register_address,
                    quality=row.quality,
                    metadata=row.metadata
                )
                readings.append(reading)
            
            return readings
    
    async def delete_old_readings(self, older_than: datetime) -> int:
        """Delete old readings and return count of deleted records."""
        with self.SessionLocal() as session:
            stmt = select(ReadingModel).where(ReadingModel.timestamp < older_than)
            old_readings = session.execute(stmt).scalars().all()
            count = len(old_readings)
            
            for reading in old_readings:
                session.delete(reading)
            
            session.commit()
            return count


class PostgreSQLConfigRepository(ConfigRepository):
    """PostgreSQL implementation of configuration repository."""
    
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=self.engine)
    
    def _model_to_entity(self, model: DeviceConfigModel) -> DeviceConfig:
        """Convert database model to domain entity."""
        registers = []
        for reg_data in model.registers:
            register = RegisterConfig(
                name=reg_data["name"],
                address=reg_data["address"],
                data_type=reg_data["data_type"],
                unit=reg_data["unit"],
                scale_factor=reg_data.get("scale_factor", 1.0),
                offset=reg_data.get("offset", 0.0),
                description=reg_data.get("description")
            )
            registers.append(register)
        
        return DeviceConfig(
            id=DeviceId(model.device_id),
            name=model.name,
            device_type=DeviceType(model.device_type),
            address=ModbusAddress(model.host, model.port),
            unit_id=model.unit_id,
            timeout=model.timeout,
            registers=registers,
            polling_interval=model.polling_interval,
            retry_count=model.retry_count,
            metadata=model.metadata
        )
    
    def _entity_to_model(self, entity: DeviceConfig) -> DeviceConfigModel:
        """Convert domain entity to database model."""
        registers_data = []
        for register in entity.registers:
            reg_data = {
                "name": register.name,
                "address": register.address,
                "data_type": register.data_type,
                "unit": register.unit,
                "scale_factor": register.scale_factor,
                "offset": register.offset,
                "description": register.description
            }
            registers_data.append(reg_data)
        
        return DeviceConfigModel(
            id=str(entity.id),
            device_id=str(entity.id),
            name=entity.name,
            device_type=str(entity.device_type),
            host=entity.address.host,
            port=entity.address.port,
            unit_id=entity.unit_id,
            timeout=entity.timeout,
            registers=registers_data,
            polling_interval=entity.polling_interval,
            retry_count=entity.retry_count,
            metadata=entity.metadata
        )
    
    async def save_config(self, config: DeviceConfig) -> None:
        """Save device configuration."""
        with self.SessionLocal() as session:
            try:
                # Check if config exists
                existing = session.get(DeviceConfigModel, str(config.id))
                if existing:
                    # Update existing config
                    existing.name = config.name
                    existing.device_type = str(config.device_type)
                    existing.host = config.address.host
                    existing.port = config.address.port
                    existing.unit_id = config.unit_id
                    existing.timeout = config.timeout
                    existing.registers = [
                        {
                            "name": reg.name,
                            "address": reg.address,
                            "data_type": reg.data_type,
                            "unit": reg.unit,
                            "scale_factor": reg.scale_factor,
                            "offset": reg.offset,
                            "description": reg.description
                        }
                        for reg in config.registers
                    ]
                    existing.polling_interval = config.polling_interval
                    existing.retry_count = config.retry_count
                    existing.metadata = config.metadata
                else:
                    # Create new config
                    model = self._entity_to_model(config)
                    session.add(model)
                
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Failed to save config: {e}")
    
    async def find_config_by_id(self, device_id: DeviceId) -> Optional[DeviceConfig]:
        """Find configuration by device ID."""
        with self.SessionLocal() as session:
            model = session.get(DeviceConfigModel, str(device_id))
            return self._model_to_entity(model) if model else None
    
    async def find_configs_by_type(self, device_type: DeviceType) -> List[DeviceConfig]:
        """Find configurations by device type."""
        with self.SessionLocal() as session:
            stmt = select(DeviceConfigModel).where(DeviceConfigModel.device_type == str(device_type))
            models = session.execute(stmt).scalars().all()
            return [self._model_to_entity(model) for model in models]
    
    async def find_all_configs(self) -> List[DeviceConfig]:
        """Find all device configurations."""
        with self.SessionLocal() as session:
            models = session.execute(select(DeviceConfigModel)).scalars().all()
            return [self._model_to_entity(model) for model in models]
    
    async def delete_config(self, device_id: DeviceId) -> bool:
        """Delete device configuration."""
        with self.SessionLocal() as session:
            model = session.get(DeviceConfigModel, str(device_id))
            if model:
                session.delete(model)
                session.commit()
                return True
            return False