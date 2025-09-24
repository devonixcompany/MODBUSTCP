"""Readings data router."""

import sys
from pathlib import Path
from fastapi import APIRouter, Request, HTTPException, Query
from typing import Optional
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from domain.value_objects import DeviceId
from ..schemas.reading import (
    ReadingResponse,
    ReadingList,
    ReadingQuery,
    ReadingCollectionRequest,
    ReadingCollectionResponse,
    ReadingStatistics,
)

router = APIRouter()


@router.get("/readings", response_model=ReadingList)
async def list_readings(
    request: Request,
    device_id: Optional[str] = Query(None, description="Filter by device ID"),
    reading_type: Optional[str] = Query(None, description="Filter by reading type"),
    start_time: Optional[datetime] = Query(None, description="Start time filter"),
    end_time: Optional[datetime] = Query(None, description="End time filter"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=1000, description="Items per page")
) -> ReadingList:
    """List readings with filtering and pagination."""
    data_collection = request.app.state.data_collection
    
    try:
        if device_id:
            readings = await data_collection.get_historical_readings(
                DeviceId(device_id),
                start_time=start_time,
                end_time=end_time,
                limit=per_page
            )
        else:
            # TODO: Implement get_all_readings method
            readings = []
        
        # Apply additional filtering
        if reading_type:
            readings = [r for r in readings if str(r.reading_type) == reading_type]
        
        # Convert to response models
        reading_responses = [
            ReadingResponse(
                device_id=str(r.device_id),
                reading_type=str(r.reading_type),
                value=r.value,
                unit=r.unit,
                timestamp=r.timestamp,
                register_address=r.register_address,
                quality=r.quality
            )
            for r in readings
        ]
        
        return ReadingList(
            readings=reading_responses,
            total=len(reading_responses),
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/readings/latest/{device_id}", response_model=list[ReadingResponse])
async def get_latest_readings(device_id: str, request: Request) -> list[ReadingResponse]:
    """Get latest readings for a specific device."""
    data_collection = request.app.state.data_collection
    
    try:
        readings = await data_collection.get_latest_readings(DeviceId(device_id))
        
        return [
            ReadingResponse(
                device_id=str(r.device_id),
                reading_type=str(r.reading_type),
                value=r.value,
                unit=r.unit,
                timestamp=r.timestamp,
                register_address=r.register_address,
                quality=r.quality
            )
            for r in readings
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/readings/collect", response_model=ReadingCollectionResponse)
async def collect_readings(
    collection_request: ReadingCollectionRequest,
    request: Request
) -> ReadingCollectionResponse:
    """Collect readings from a specific device."""
    data_collection = request.app.state.data_collection
    
    try:
        readings = await data_collection.collect_device_data(
            DeviceId(collection_request.device_id)
        )
        
        return ReadingCollectionResponse(
            device_id=collection_request.device_id,
            readings_collected=len(readings),
            success=len(readings) > 0,
            message=f"Collected {len(readings)} readings" if readings else "No readings collected",
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/readings/collect-all", response_model=list[ReadingCollectionResponse])
async def collect_all_readings(request: Request) -> list[ReadingCollectionResponse]:
    """Collect readings from all connected devices."""
    data_collection = request.app.state.data_collection
    
    try:
        results = await data_collection.collect_all_devices_data()
        
        responses = []
        for device_id, readings in results.items():
            responses.append(
                ReadingCollectionResponse(
                    device_id=str(device_id),
                    readings_collected=len(readings),
                    success=len(readings) > 0,
                    message=f"Collected {len(readings)} readings" if readings else "No readings collected",
                    timestamp=datetime.utcnow()
                )
            )
        
        return responses
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/readings/statistics/{device_id}", response_model=list[ReadingStatistics])
async def get_reading_statistics(
    device_id: str,
    request: Request,
    hours: int = Query(24, description="Hours of data to analyze", ge=1, le=8760)
) -> list[ReadingStatistics]:
    """Get reading statistics for a device."""
    data_collection = request.app.state.data_collection
    
    try:
        # Get historical readings
        start_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        start_time = start_time.replace(hour=start_time.hour - hours)
        
        readings = await data_collection.get_historical_readings(
            DeviceId(device_id),
            start_time=start_time
        )
        
        # Group by reading type and calculate statistics
        stats_by_type = {}
        for reading in readings:
            reading_type = str(reading.reading_type)
            if reading_type not in stats_by_type:
                stats_by_type[reading_type] = []
            stats_by_type[reading_type].append(reading)
        
        statistics = []
        for reading_type, type_readings in stats_by_type.items():
            values = [r.value for r in type_readings if r.value is not None]
            if values:
                statistics.append(
                    ReadingStatistics(
                        device_id=device_id,
                        reading_type=reading_type,
                        count=len(values),
                        min_value=min(values),
                        max_value=max(values),
                        avg_value=sum(values) / len(values),
                        latest_value=type_readings[-1].value,
                        latest_timestamp=type_readings[-1].timestamp
                    )
                )
        
        return statistics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))