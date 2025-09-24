"""Device management router."""

import sys
from pathlib import Path
from fastapi import APIRouter, Request, HTTPException, Query, Depends
from typing import List, Optional
import time

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from domain.value_objects import DeviceId, DeviceType, ModbusAddress
from infrastructure.modbus import PyModbusClient
from ..schemas.device import (
    DeviceCreate,
    DeviceResponse,
    DeviceUpdate,
    DeviceList,
    DeviceConnectionTest,
    DeviceConnectionTestResponse,
)

router = APIRouter()


@router.post("/devices", response_model=DeviceResponse, status_code=201)
async def create_device(device_data: DeviceCreate, request: Request) -> DeviceResponse:
    """Create a new MODBUS device."""
    device_mgmt = request.app.state.device_mgmt
    
    try:
        device = await device_mgmt.add_device(
            name=device_data.name,
            device_type=DeviceType(device_data.device_type),
            address=ModbusAddress(device_data.host, device_data.port),
            unit_id=device_data.unit_id
        )
        
        return DeviceResponse(
            id=str(device.id),
            name=device.name,
            device_type=str(device.device_type),
            host=device.address.host,
            port=device.address.port,
            unit_id=device.unit_id,
            timeout=device_data.timeout,
            status=device.status,
            metadata=device.metadata or {},
            created_at="2024-01-01T00:00:00Z",  # TODO: Add timestamps to entity
            updated_at="2024-01-01T00:00:00Z"
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/devices", response_model=DeviceList)
async def list_devices(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=1000, description="Items per page"),
    device_type: Optional[str] = Query(None, description="Filter by device type")
) -> DeviceList:
    """List all devices with pagination."""
    device_mgmt = request.app.state.device_mgmt
    
    try:
        devices = await device_mgmt.list_devices()
        
        # Apply filtering
        if device_type:
            devices = [d for d in devices if str(d.device_type) == device_type]
        
        # Apply pagination
        total = len(devices)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_devices = devices[start_idx:end_idx]
        
        device_responses = [
            DeviceResponse(
                id=str(d.id),
                name=d.name,
                device_type=str(d.device_type),
                host=d.address.host,
                port=d.address.port,
                unit_id=d.unit_id,
                timeout=3,  # TODO: Add to entity
                status=d.status,
                metadata=d.metadata or {},
                created_at="2024-01-01T00:00:00Z",
                updated_at="2024-01-01T00:00:00Z"
            )
            for d in paginated_devices
        ]
        
        return DeviceList(
            devices=device_responses,
            total=total,
            page=page,
            per_page=per_page
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/devices/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: str, request: Request) -> DeviceResponse:
    """Get device by ID."""
    device_mgmt = request.app.state.device_mgmt
    
    try:
        device = await device_mgmt.get_device(DeviceId(device_id))
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        return DeviceResponse(
            id=str(device.id),
            name=device.name,
            device_type=str(device.device_type),
            host=device.address.host,
            port=device.address.port,
            unit_id=device.unit_id,
            timeout=3,  # TODO: Add to entity
            status=device.status,
            metadata=device.metadata or {},
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/devices/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: str,
    device_update: DeviceUpdate,
    request: Request
) -> DeviceResponse:
    """Update device information."""
    device_mgmt = request.app.state.device_mgmt
    
    try:
        device = await device_mgmt.get_device(DeviceId(device_id))
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        # Update fields if provided
        if device_update.name is not None:
            device.name = device_update.name
        if device_update.metadata is not None:
            device.metadata = device_update.metadata
        
        # Save updated device (assuming we add an update method)
        # await device_mgmt.update_device(device)
        
        return DeviceResponse(
            id=str(device.id),
            name=device.name,
            device_type=str(device.device_type),
            host=device.address.host,
            port=device.address.port,
            unit_id=device.unit_id,
            timeout=device_update.timeout or 3,
            status=device.status,
            metadata=device.metadata or {},
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/devices/{device_id}", status_code=204)
async def delete_device(device_id: str, request: Request):
    """Delete a device."""
    device_mgmt = request.app.state.device_mgmt
    
    try:
        success = await device_mgmt.remove_device(DeviceId(device_id))
        if not success:
            raise HTTPException(status_code=404, detail="Device not found")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/devices/{device_id}/connect", status_code=200)
async def connect_device(device_id: str, request: Request):
    """Connect to a device."""
    device_mgmt = request.app.state.device_mgmt
    
    try:
        success = await device_mgmt.connect_device(DeviceId(device_id))
        if not success:
            raise HTTPException(status_code=400, detail="Failed to connect to device")
        
        return {"message": "Device connected successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/devices/{device_id}/disconnect", status_code=200)
async def disconnect_device(device_id: str, request: Request):
    """Disconnect from a device."""
    device_mgmt = request.app.state.device_mgmt
    
    try:
        success = await device_mgmt.disconnect_device(DeviceId(device_id))
        if not success:
            raise HTTPException(status_code=400, detail="Failed to disconnect from device")
        
        return {"message": "Device disconnected successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/devices/test-connection", response_model=DeviceConnectionTestResponse)
async def test_connection(test_data: DeviceConnectionTest) -> DeviceConnectionTestResponse:
    """Test connection to a MODBUS device."""
    client = PyModbusClient()
    
    try:
        start_time = time.time()
        address = ModbusAddress(test_data.host, test_data.port)
        success = await client.connect(address, test_data.unit_id, test_data.timeout)
        response_time = time.time() - start_time
        
        if success:
            await client.disconnect()
            return DeviceConnectionTestResponse(
                success=True,
                message="Connection successful",
                response_time=response_time
            )
        else:
            return DeviceConnectionTestResponse(
                success=False,
                message="Connection failed",
                response_time=response_time,
                error="Unable to establish connection"
            )
            
    except Exception as e:
        return DeviceConnectionTestResponse(
            success=False,
            message="Connection test failed",
            error=str(e)
        )