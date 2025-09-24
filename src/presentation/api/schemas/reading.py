"""Reading API schemas."""

import sys
from pathlib import Path
from typing import Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


class ReadingResponse(BaseModel):
    """Schema for reading response."""
    device_id: str = Field(..., description="Device unique identifier")
    reading_type: str = Field(..., description="Type of reading (voltage, current, temperature, etc.)")
    value: Union[float, int] = Field(..., description="Reading value")
    unit: str = Field(..., description="Unit of measurement")
    timestamp: datetime = Field(..., description="Reading timestamp")
    register_address: int = Field(..., description="MODBUS register address")
    quality: Optional[str] = Field(None, description="Reading quality indicator")
    
    class Config:
        from_attributes = True


class ReadingList(BaseModel):
    """Schema for reading list response."""
    readings: list[ReadingResponse] = Field(..., description="List of readings")
    total: int = Field(..., description="Total number of readings")
    page: int = Field(1, description="Current page number")
    per_page: int = Field(50, description="Items per page")


class ReadingQuery(BaseModel):
    """Schema for reading query parameters."""
    device_id: Optional[str] = Field(None, description="Filter by device ID")
    reading_type: Optional[str] = Field(None, description="Filter by reading type")
    start_time: Optional[datetime] = Field(None, description="Start time for filtering")
    end_time: Optional[datetime] = Field(None, description="End time for filtering")
    page: int = Field(1, description="Page number", ge=1)
    per_page: int = Field(50, description="Items per page", ge=1, le=1000)


class ReadingCollectionRequest(BaseModel):
    """Schema for requesting data collection from a device."""
    device_id: str = Field(..., description="Device unique identifier")


class ReadingCollectionResponse(BaseModel):
    """Schema for data collection response."""
    device_id: str = Field(..., description="Device unique identifier")
    readings_collected: int = Field(..., description="Number of readings collected")
    success: bool = Field(..., description="Whether collection was successful")
    message: str = Field(..., description="Collection result message")
    timestamp: datetime = Field(..., description="Collection timestamp")


class ReadingStatistics(BaseModel):
    """Schema for reading statistics."""
    device_id: str = Field(..., description="Device unique identifier")
    reading_type: str = Field(..., description="Type of reading")
    count: int = Field(..., description="Number of readings")
    min_value: Optional[Union[float, int]] = Field(None, description="Minimum value")
    max_value: Optional[Union[float, int]] = Field(None, description="Maximum value") 
    avg_value: Optional[float] = Field(None, description="Average value")
    latest_value: Optional[Union[float, int]] = Field(None, description="Latest value")
    latest_timestamp: Optional[datetime] = Field(None, description="Latest reading timestamp")