"""Device management CLI commands."""

import asyncio
from typing import List
import click
from tabulate import tabulate

from ....domain.value_objects import DeviceId, DeviceType, ModbusAddress


class DeviceCommands:
    """Device management commands."""
    
    def create_group(self):
        """Create device command group."""
        
        @click.group(name='device')
        def device_group():
            """Device management commands."""
            pass
        
        @device_group.command()
        @click.option('--name', required=True, help='Device name')
        @click.option('--type', 'device_type', required=True, 
                     type=click.Choice(['SDM120', 'PM2510-0D', 'XY-MD02', 'GENERIC']),
                     help='Device type')
        @click.option('--host', required=True, help='Device host address')
        @click.option('--port', default=502, help='Device port')
        @click.option('--unit', required=True, type=int, help='MODBUS unit ID')
        @click.pass_context
        def add(ctx, name: str, device_type: str, host: str, port: int, unit: int):
            """Add a new device."""
            
            async def _add():
                device_mgmt = ctx.obj['device_mgmt']
                
                try:
                    device = await device_mgmt.add_device(
                        name=name,
                        device_type=DeviceType(device_type),
                        address=ModbusAddress(host, port),
                        unit_id=unit
                    )
                    
                    click.echo(f"✅ Added device: {device.name} (ID: {device.id})")
                    
                except Exception as e:
                    click.echo(f"❌ Error adding device: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_add())
            if not success:
                ctx.exit(1)
        
        @device_group.command()
        @click.argument('device_id')
        @click.pass_context
        def remove(ctx, device_id: str):
            """Remove a device."""
            
            async def _remove():
                device_mgmt = ctx.obj['device_mgmt']
                
                try:
                    success = await device_mgmt.remove_device(DeviceId(device_id))
                    if success:
                        click.echo(f"✅ Removed device: {device_id}")
                    else:
                        click.echo(f"❌ Device not found: {device_id}")
                        return False
                        
                except Exception as e:
                    click.echo(f"❌ Error removing device: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_remove())
            if not success:
                ctx.exit(1)
        
        @device_group.command()
        @click.pass_context
        def list(ctx):
            """List all devices."""
            
            async def _list():
                device_mgmt = ctx.obj['device_mgmt']
                
                try:
                    devices = await device_mgmt.list_devices()
                    
                    if not devices:
                        click.echo("No devices found.")
                        return
                    
                    # Prepare table data
                    headers = ['ID', 'Name', 'Type', 'Address', 'Unit', 'Status']
                    rows = []
                    
                    for device in devices:
                        rows.append([
                            str(device.id)[:8] + '...',  # Truncate ID for display
                            device.name,
                            str(device.device_type),
                            str(device.address),
                            device.unit_id,
                            device.status.value
                        ])
                    
                    click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
                    
                except Exception as e:
                    click.echo(f"❌ Error listing devices: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_list())
            if not success:
                ctx.exit(1)
        
        @device_group.command()
        @click.argument('device_id')
        @click.option('--timeout', default=3, help='Connection timeout')
        @click.pass_context
        def connect(ctx, device_id: str, timeout: int):
            """Connect to a device."""
            
            async def _connect():
                device_mgmt = ctx.obj['device_mgmt']
                
                try:
                    click.echo(f"Connecting to device {device_id}...")
                    success = await device_mgmt.connect_device(DeviceId(device_id), timeout)
                    
                    if success:
                        click.echo(f"✅ Connected to device: {device_id}")
                    else:
                        click.echo(f"❌ Failed to connect to device: {device_id}")
                        return False
                        
                except Exception as e:
                    click.echo(f"❌ Error connecting to device: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_connect())
            if not success:
                ctx.exit(1)
        
        @device_group.command()
        @click.argument('device_id')
        @click.pass_context
        def disconnect(ctx, device_id: str):
            """Disconnect from a device."""
            
            async def _disconnect():
                device_mgmt = ctx.obj['device_mgmt']
                
                try:
                    success = await device_mgmt.disconnect_device(DeviceId(device_id))
                    
                    if success:
                        click.echo(f"✅ Disconnected from device: {device_id}")
                    else:
                        click.echo(f"❌ Failed to disconnect from device: {device_id}")
                        return False
                        
                except Exception as e:
                    click.echo(f"❌ Error disconnecting from device: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_disconnect())
            if not success:
                ctx.exit(1)
        
        @device_group.command()
        @click.argument('device_id')
        @click.pass_context
        def info(ctx, device_id: str):
            """Show device information."""
            
            async def _info():
                device_mgmt = ctx.obj['device_mgmt']
                
                try:
                    device = await device_mgmt.get_device(DeviceId(device_id))
                    
                    if not device:
                        click.echo(f"❌ Device not found: {device_id}")
                        return False
                    
                    click.echo(f"Device Information")
                    click.echo("=" * 50)
                    click.echo(f"ID: {device.id}")
                    click.echo(f"Name: {device.name}")
                    click.echo(f"Type: {device.device_type}")
                    click.echo(f"Address: {device.address}")
                    click.echo(f"Unit ID: {device.unit_id}")
                    click.echo(f"Status: {device.status.value}")
                    
                    if device.metadata:
                        click.echo(f"Metadata: {device.metadata}")
                    
                except Exception as e:
                    click.echo(f"❌ Error getting device info: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_info())
            if not success:
                ctx.exit(1)
        
        return device_group