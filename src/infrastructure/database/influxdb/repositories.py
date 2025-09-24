"""InfluxDB repository implementations."""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import logging

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from domain.entities import Reading
from domain.repositories import ReadingRepository
from domain.value_objects import DeviceId, ReadingType

logger = logging.getLogger(__name__)


class InfluxDBReadingRepository(ReadingRepository):
    """InfluxDB implementation for reading repository (time-series data)."""
    
    def __init__(self, url: str, token: str, org: str, bucket: str):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket
        
        try:
            self.client = InfluxDBClient(url=url, token=token, org=org)
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.query_api = self.client.query_api()
            
            # Test connection
            self.client.ping()
            logger.info(f"Connected to InfluxDB at {url}")
        except Exception as e:
            logger.error(f"Failed to connect to InfluxDB: {e}")
            raise
    
    def _entity_to_point(self, entity: Reading) -> Point:
        """Convert Reading entity to InfluxDB Point."""
        point = (
            Point("readings")
            .tag("device_id", str(entity.device_id))
            .tag("reading_type", str(entity.reading_type))
            .tag("unit", entity.unit)
            .field("value", float(entity.value))
            .field("register_address", entity.register_address)
            .time(entity.timestamp)
        )
        
        if entity.quality:
            point = point.tag("quality", entity.quality)
        
        if entity.metadata:
            for key, value in entity.metadata.items():
                if isinstance(value, (str, int, float, bool)):
                    point = point.field(f"meta_{key}", value)
        
        return point
    
    def _record_to_entity(self, record) -> Reading:
        """Convert InfluxDB record to Reading entity."""
        return Reading(
            device_id=DeviceId(record["device_id"]),
            reading_type=ReadingType(record["reading_type"]),
            value=record["_value"],
            unit=record["unit"],
            timestamp=record["_time"],
            register_address=int(record["register_address"]),
            quality=record.get("quality"),
            metadata={
                key.replace("meta_", ""): value 
                for key, value in record.items() 
                if key.startswith("meta_")
            } or None
        )
    
    async def save(self, reading: Reading) -> None:
        """Save a reading."""
        try:
            point = self._entity_to_point(reading)
            self.write_api.write(bucket=self.bucket, record=point)
        except Exception as e:
            logger.error(f"Failed to save reading to InfluxDB: {e}")
            raise
    
    async def save_batch(self, readings: List[Reading]) -> None:
        """Save multiple readings."""
        try:
            points = [self._entity_to_point(reading) for reading in readings]
            self.write_api.write(bucket=self.bucket, record=points)
        except Exception as e:
            logger.error(f"Failed to save batch readings to InfluxDB: {e}")
            raise
    
    async def find_by_device(
        self,
        device_id: DeviceId,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Reading]:
        """Find readings by device."""
        try:
            # Build Flux query
            query = f'''
                from(bucket: "{self.bucket}")
                |> range(start: {self._format_time(start_time) if start_time else "-30d"}, 
                        stop: {self._format_time(end_time) if end_time else "now()"})
                |> filter(fn: (r) => r._measurement == "readings")
                |> filter(fn: (r) => r.device_id == "{device_id}")
                |> filter(fn: (r) => r._field == "value")
                |> sort(columns: ["_time"], desc: true)
            '''
            
            if limit:
                query += f'|> limit(n: {limit})'
            
            # Execute query
            tables = self.query_api.query(query)
            
            readings = []
            for table in tables:
                for record in table.records:
                    try:
                        reading = self._record_to_entity(record.values)
                        readings.append(reading)
                    except Exception as e:
                        logger.warning(f"Failed to convert record to reading: {e}")
                        continue
            
            return readings
            
        except Exception as e:
            logger.error(f"Failed to query readings from InfluxDB: {e}")
            return []
    
    async def find_by_type(
        self,
        reading_type: ReadingType,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Reading]:
        """Find readings by type."""
        try:
            # Build Flux query
            query = f'''
                from(bucket: "{self.bucket}")
                |> range(start: {self._format_time(start_time) if start_time else "-30d"}, 
                        stop: {self._format_time(end_time) if end_time else "now()"})
                |> filter(fn: (r) => r._measurement == "readings")
                |> filter(fn: (r) => r.reading_type == "{reading_type}")
                |> filter(fn: (r) => r._field == "value")
                |> sort(columns: ["_time"], desc: true)
            '''
            
            if limit:
                query += f'|> limit(n: {limit})'
            
            # Execute query
            tables = self.query_api.query(query)
            
            readings = []
            for table in tables:
                for record in table.records:
                    try:
                        reading = self._record_to_entity(record.values)
                        readings.append(reading)
                    except Exception as e:
                        logger.warning(f"Failed to convert record to reading: {e}")
                        continue
            
            return readings
            
        except Exception as e:
            logger.error(f"Failed to query readings by type from InfluxDB: {e}")
            return []
    
    async def find_latest_by_device(self, device_id: DeviceId) -> List[Reading]:
        """Find latest readings for a device."""
        try:
            # Get latest reading for each reading type
            query = f'''
                from(bucket: "{self.bucket}")
                |> range(start: -24h)
                |> filter(fn: (r) => r._measurement == "readings")
                |> filter(fn: (r) => r.device_id == "{device_id}")
                |> filter(fn: (r) => r._field == "value")
                |> group(columns: ["reading_type"])
                |> last()
                |> sort(columns: ["_time"], desc: true)
            '''
            
            # Execute query
            tables = self.query_api.query(query)
            
            readings = []
            for table in tables:
                for record in table.records:
                    try:
                        reading = self._record_to_entity(record.values)
                        readings.append(reading)
                    except Exception as e:
                        logger.warning(f"Failed to convert record to reading: {e}")
                        continue
            
            return readings
            
        except Exception as e:
            logger.error(f"Failed to query latest readings from InfluxDB: {e}")
            return []
    
    async def delete_old_readings(self, older_than: datetime) -> int:
        """Delete old readings and return count of deleted records."""
        try:
            # InfluxDB automatically handles data retention based on bucket policies
            # This is a placeholder implementation
            logger.info(f"InfluxDB data retention should be configured at bucket level")
            return 0
            
        except Exception as e:
            logger.error(f"Failed to delete old readings from InfluxDB: {e}")
            return 0
    
    def _format_time(self, dt: datetime) -> str:
        """Format datetime for InfluxDB Flux query."""
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def close(self):
        """Close InfluxDB connection."""
        if hasattr(self, 'client'):
            self.client.close()