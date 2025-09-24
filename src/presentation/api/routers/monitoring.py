"""Monitoring and health check router."""

import sys
from pathlib import Path
from fastapi import APIRouter, Request, HTTPException
from typing import List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from domain.value_objects import DeviceId
from ..schemas.monitoring import (
    HealthCheckResponse,
    MonitoringStatus,
    MonitoringStartRequest,
    MonitoringStartResponse,
    MonitoringStopResponse,
    SystemHealth,
)

router = APIRouter()


@router.get("/monitoring/health/{device_id}", response_model=HealthCheckResponse)
async def check_device_health(device_id: str, request: Request) -> HealthCheckResponse:
    """Check health status of a specific device."""
    monitoring = request.app.state.monitoring
    
    try:
        health_info = await monitoring.check_device_health(DeviceId(device_id))
        
        return HealthCheckResponse(
            device_id=device_id,
            device_name=health_info.get("device_name", "Unknown"),
            device_type=health_info.get("device_type", "Unknown"),
            status=health_info.get("status", "unknown"),
            connection_status=health_info.get("connection_status", "unknown"),
            responsive=health_info.get("responsive", False),
            has_recent_data=health_info.get("has_recent_data", False),
            last_reading=health_info.get("last_reading"),
            last_check=health_info.get("last_check", "2024-01-01T00:00:00Z"),
            message=health_info.get("message", "")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monitoring/health", response_model=List[HealthCheckResponse])
async def check_all_devices_health(request: Request) -> List[HealthCheckResponse]:
    """Check health status of all devices."""
    monitoring = request.app.state.monitoring
    
    try:
        health_checks = await monitoring.check_all_devices_health()
        
        return [
            HealthCheckResponse(
                device_id=health.get("device_id", "unknown"),
                device_name=health.get("device_name", "Unknown"),
                device_type=health.get("device_type", "Unknown"),
                status=health.get("status", "unknown"),
                connection_status=health.get("connection_status", "unknown"),
                responsive=health.get("responsive", False),
                has_recent_data=health.get("has_recent_data", False),
                last_reading=health.get("last_reading"),
                last_check=health.get("last_check", "2024-01-01T00:00:00Z"),
                message=health.get("message", "")
            )
            for health in health_checks
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/monitoring/start", response_model=MonitoringStartResponse)
async def start_monitoring(
    monitoring_request: MonitoringStartRequest,
    request: Request
) -> MonitoringStartResponse:
    """Start monitoring a device."""
    monitoring = request.app.state.monitoring
    
    try:
        success = await monitoring.start_monitoring(
            DeviceId(monitoring_request.device_id),
            monitoring_request.interval
        )
        
        return MonitoringStartResponse(
            device_id=monitoring_request.device_id,
            success=success,
            message="Monitoring started successfully" if success else "Failed to start monitoring",
            interval=monitoring_request.interval
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/monitoring/stop/{device_id}", response_model=MonitoringStopResponse)
async def stop_monitoring(device_id: str, request: Request) -> MonitoringStopResponse:
    """Stop monitoring a device."""
    monitoring = request.app.state.monitoring
    
    try:
        success = await monitoring.stop_monitoring(DeviceId(device_id))
        
        return MonitoringStopResponse(
            device_id=device_id,
            success=success,
            message="Monitoring stopped successfully" if success else "Failed to stop monitoring"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monitoring/status", response_model=MonitoringStatus)
async def get_monitoring_status(request: Request) -> MonitoringStatus:
    """Get monitoring status for all devices."""
    monitoring = request.app.state.monitoring
    
    try:
        status_info = await monitoring.get_monitoring_status()
        
        return MonitoringStatus(
            total_monitored_devices=status_info.get("total_monitored_devices", 0),
            monitored_devices=status_info.get("monitored_devices", []),
            timestamp=status_info.get("timestamp", "2024-01-01T00:00:00Z")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/monitoring/stop-all", status_code=200)
async def stop_all_monitoring(request: Request):
    """Stop monitoring all devices."""
    monitoring = request.app.state.monitoring
    
    try:
        await monitoring.stop_all_monitoring()
        return {"message": "All monitoring stopped successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monitoring/system-health", response_model=SystemHealth)
async def get_system_health(request: Request) -> SystemHealth:
    """Get overall system health status."""
    monitoring = request.app.state.monitoring
    device_mgmt = request.app.state.device_mgmt
    
    try:
        # Get all devices
        devices = await device_mgmt.list_devices()
        total_devices = len(devices)
        connected_devices = len([d for d in devices if d.is_connected()])
        
        # Get health checks
        health_checks = await monitoring.check_all_devices_health()
        healthy_devices = len([h for h in health_checks if h.get("status") == "healthy"])
        
        # Get monitoring status
        monitoring_status = await monitoring.get_monitoring_status()
        monitored_devices = monitoring_status.get("total_monitored_devices", 0)
        
        # Determine overall status
        if healthy_devices == total_devices and total_devices > 0:
            overall_status = "healthy"
        elif healthy_devices > total_devices * 0.8:
            overall_status = "warning"
        else:
            overall_status = "critical"
        
        return SystemHealth(
            status=overall_status,
            total_devices=total_devices,
            healthy_devices=healthy_devices,
            connected_devices=connected_devices,
            monitored_devices=monitored_devices,
            last_check="2024-01-01T00:00:00Z"  # TODO: Add actual timestamp
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))