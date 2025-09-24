"""Device API schemas."""

import sys
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from domain.entities.device import DeviceStatus


class DeviceBase(BaseModel):
    """Base device schema."""
    name: str = Field(..., description="Device name")
    device_type: str = Field(..., description="Device type (SDM120, PM2510-0D, XY-MD02, GENERIC)")
    host: str = Field(..., description="MODBUS TCP host address")
    port: int = Field(502, description="MODBUS TCP port")
    unit_id: int = Field(..., description="MODBUS unit ID", ge=1, le=247)
    timeout: int = Field(3, description="Connection timeout in seconds", ge=1, le=60)
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional device metadata")


class DeviceCreate(DeviceBase):
    """Schema for creating a new device."""
    pass


class DeviceUpdate(BaseModel):
    """Schema for updating device information."""
    name: Optional[str] = Field(None, description="Device name")
    timeout: Optional[int] = Field(None, description="Connection timeout in seconds", ge=1, le=60)
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional device metadata")


class DeviceResponse(DeviceBase):
    """Schema for device response."""
    id: str = Field(..., description="Device unique identifier")
    status: DeviceStatus = Field(..., description="Device connection status")
    created_at: datetime = Field(..., description="Device creation timestamp")
    updated_at: datetime = Field(..., description="Device last update timestamp")
    
    class Config:
        from_attributes = True
        use_enum_values = True


class DeviceList(BaseModel):
    """Schema for device list response."""
    devices: list[DeviceResponse] = Field(..., description="List of devices")
    total: int = Field(..., description="Total number of devices")
    page: int = Field(1, description="Current page number")
    per_page: int = Field(50, description="Items per page")


class DeviceConnectionTest(BaseModel):
    """Schema for device connection test."""
    host: str = Field(..., description="MODBUS TCP host address")
    port: int = Field(502, description="MODBUS TCP port")
    unit_id: int = Field(..., description="MODBUS unit ID", ge=1, le=247)
    timeout: int = Field(3, description="Connection timeout in seconds", ge=1, le=60)


class DeviceConnectionTestResponse(BaseModel):
    """Schema for device connection test response."""
    success: bool = Field(..., description="Whether connection was successful")
    message: str = Field(..., description="Connection test result message")
    response_time: Optional[float] = Field(None, description="Response time in seconds")
    error: Optional[str] = Field(None, description="Error message if connection failed")