"""Monitoring CLI commands."""

import asyncio
import json
import click
from tabulate import tabulate

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from domain.value_objects import DeviceId


class MonitoringCommands:
    """Monitoring commands."""
    
    def create_group(self):
        """Create monitoring command group."""
        
        @click.group(name='monitor')
        def monitor_group():
            """Device monitoring commands."""
            pass
        
        @monitor_group.command()
        @click.argument('device_id')
        @click.pass_context
        def health(ctx, device_id: str):
            """Check health status of a device."""
            
            async def _health():
                monitoring = ctx.obj['monitoring']
                
                try:
                    health_info = await monitoring.check_device_health(DeviceId(device_id))
                    
                    click.echo(f"Health Check - {health_info.get('device_name', 'Unknown')}")
                    click.echo("=" * 50)
                    
                    status = health_info.get('status', 'unknown')
                    status_icon = {
                        'healthy': '✅',
                        'disconnected': '⚠️',
                        'connection_error': '❌',
                        'error': '❌',
                        'not_found': '❌'
                    }.get(status, '❓')
                    
                    click.echo(f"Status: {status_icon} {status.upper()}")
                    click.echo(f"Connection: {'✅ Connected' if health_info.get('connection_status') == 'connected' else '❌ Disconnected'}")
                    click.echo(f"Responsive: {'✅ Yes' if health_info.get('responsive') else '❌ No'}")
                    click.echo(f"Recent Data: {'✅ Yes' if health_info.get('has_recent_data') else '❌ No'}")
                    
                    if health_info.get('last_reading'):
                        click.echo(f"Last Reading: {health_info['last_reading']}")
                    
                    if health_info.get('message'):
                        click.echo(f"Message: {health_info['message']}")
                    
                    click.echo(f"Last Check: {health_info.get('last_check', 'Unknown')}")
                    
                except Exception as e:
                    click.echo(f"❌ Error checking device health: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_health())
            if not success:
                ctx.exit(1)
        
        @monitor_group.command()
        @click.pass_context
        def health_all(ctx):
            """Check health status of all devices."""
            
            async def _health_all():
                monitoring = ctx.obj['monitoring']
                
                try:
                    health_checks = await monitoring.check_all_devices_health()
                    
                    if not health_checks:
                        click.echo("No devices found.")
                        return True
                    
                    click.echo("Health Status - All Devices")
                    click.echo("=" * 70)
                    
                    # Prepare table data
                    headers = ['Device', 'Type', 'Status', 'Connected', 'Responsive', 'Recent Data']
                    rows = []
                    
                    for health in health_checks:
                        status = health.get('status', 'unknown')
                        status_icon = {
                            'healthy': '✅',
                            'disconnected': '⚠️',
                            'connection_error': '❌',
                            'error': '❌',
                            'not_found': '❌'
                        }.get(status, '❓')
                        
                        rows.append([
                            health.get('device_name', 'Unknown'),
                            health.get('device_type', 'Unknown'),
                            f"{status_icon} {status}",
                            '✅' if health.get('connection_status') == 'connected' else '❌',
                            '✅' if health.get('responsive') else '❌',
                            '✅' if health.get('has_recent_data') else '❌'
                        ])
                    
                    click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
                    
                    # Summary
                    healthy_count = sum(1 for h in health_checks if h.get('status') == 'healthy')
                    total_count = len(health_checks)
                    
                    click.echo(f"\nSummary: {healthy_count}/{total_count} devices healthy")
                    
                except Exception as e:
                    click.echo(f"❌ Error checking devices health: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_health_all())
            if not success:
                ctx.exit(1)
        
        @monitor_group.command()
        @click.argument('device_id')
        @click.option('--interval', default=30, help='Monitoring interval in seconds')
        @click.pass_context
        def start(ctx, device_id: str, interval: int):
            """Start monitoring a device."""
            
            async def _start():
                monitoring = ctx.obj['monitoring']
                
                try:
                    success = await monitoring.start_monitoring(DeviceId(device_id), interval)
                    
                    if success:
                        click.echo(f"✅ Started monitoring device: {device_id} (interval: {interval}s)")
                    else:
                        click.echo(f"❌ Failed to start monitoring device: {device_id}")
                        return False
                        
                except Exception as e:
                    click.echo(f"❌ Error starting monitoring: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_start())
            if not success:
                ctx.exit(1)
        
        @monitor_group.command()
        @click.argument('device_id')
        @click.pass_context
        def stop(ctx, device_id: str):
            """Stop monitoring a device."""
            
            async def _stop():
                monitoring = ctx.obj['monitoring']
                
                try:
                    success = await monitoring.stop_monitoring(DeviceId(device_id))
                    
                    if success:
                        click.echo(f"✅ Stopped monitoring device: {device_id}")
                    else:
                        click.echo(f"❌ Device was not being monitored: {device_id}")
                        return False
                        
                except Exception as e:
                    click.echo(f"❌ Error stopping monitoring: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_stop())
            if not success:
                ctx.exit(1)
        
        @monitor_group.command()
        @click.pass_context
        def status(ctx):
            """Show monitoring status."""
            
            async def _status():
                monitoring = ctx.obj['monitoring']
                
                try:
                    status_info = await monitoring.get_monitoring_status()
                    
                    click.echo("Monitoring Status")
                    click.echo("=" * 50)
                    click.echo(f"Total Monitored Devices: {status_info.get('total_monitored_devices', 0)}")
                    click.echo(f"Timestamp: {status_info.get('timestamp', 'Unknown')}")
                    
                    monitored_devices = status_info.get('monitored_devices', [])
                    
                    if monitored_devices:
                        click.echo("\nMonitored Devices:")
                        headers = ['Device ID', 'Device Name', 'Task Status']
                        rows = []
                        
                        for device in monitored_devices:
                            status_icon = '✅' if device.get('task_running') else '❌'
                            task_status = 'Running' if device.get('task_running') else 'Stopped'
                            
                            rows.append([
                                device.get('device_id', 'Unknown')[:8] + '...',
                                device.get('device_name', 'Unknown'),
                                f"{status_icon} {task_status}"
                            ])
                        
                        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
                    else:
                        click.echo("\nNo devices are currently being monitored.")
                    
                except Exception as e:
                    click.echo(f"❌ Error getting monitoring status: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_status())
            if not success:
                ctx.exit(1)
        
        @monitor_group.command()
        @click.pass_context
        def stop_all(ctx):
            """Stop monitoring all devices."""
            
            async def _stop_all():
                monitoring = ctx.obj['monitoring']
                
                try:
                    await monitoring.stop_all_monitoring()
                    click.echo("✅ Stopped monitoring all devices")
                    
                except Exception as e:
                    click.echo(f"❌ Error stopping all monitoring: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_stop_all())
            if not success:
                ctx.exit(1)
        
        return monitor_group