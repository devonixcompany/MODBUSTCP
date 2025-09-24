"""Monitoring API schemas."""

import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


class HealthCheckResponse(BaseModel):
    """Schema for device health check response."""
    device_id: str = Field(..., description="Device unique identifier")
    device_name: str = Field(..., description="Device name")
    device_type: str = Field(..., description="Device type")
    status: str = Field(..., description="Health status (healthy, disconnected, error, etc.)")
    connection_status: str = Field(..., description="Connection status") 
    responsive: bool = Field(..., description="Whether device is responding")
    has_recent_data: bool = Field(..., description="Whether device has recent data")
    last_reading: Optional[datetime] = Field(None, description="Timestamp of last reading")
    last_check: datetime = Field(..., description="Timestamp of health check")
    message: str = Field(..., description="Health check message")


class MonitoringStatus(BaseModel):
    """Schema for monitoring status response."""
    total_monitored_devices: int = Field(..., description="Total number of monitored devices")
    monitored_devices: List[Dict[str, Any]] = Field(..., description="List of monitored devices")
    timestamp: datetime = Field(..., description="Status timestamp")


class MonitoringStartRequest(BaseModel):
    """Schema for starting device monitoring."""
    device_id: str = Field(..., description="Device unique identifier")
    interval: int = Field(30, description="Monitoring interval in seconds", ge=5, le=3600)


class MonitoringStartResponse(BaseModel):
    """Schema for monitoring start response."""
    device_id: str = Field(..., description="Device unique identifier")
    success: bool = Field(..., description="Whether monitoring was started successfully")
    message: str = Field(..., description="Start monitoring result message")
    interval: int = Field(..., description="Monitoring interval in seconds")


class MonitoringStopResponse(BaseModel):
    """Schema for monitoring stop response."""
    device_id: str = Field(..., description="Device unique identifier")
    success: bool = Field(..., description="Whether monitoring was stopped successfully")
    message: str = Field(..., description="Stop monitoring result message")


class SystemHealth(BaseModel):
    """Schema for overall system health."""
    status: str = Field(..., description="Overall system status")
    total_devices: int = Field(..., description="Total number of devices")
    healthy_devices: int = Field(..., description="Number of healthy devices")
    connected_devices: int = Field(..., description="Number of connected devices")
    monitored_devices: int = Field(..., description="Number of monitored devices")
    last_check: datetime = Field(..., description="Last system health check timestamp")