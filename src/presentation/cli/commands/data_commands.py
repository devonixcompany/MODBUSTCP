"""Data collection CLI commands."""

import asyncio
from datetime import datetime, timedelta
import click
from tabulate import tabulate

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from domain.value_objects import DeviceId


class DataCommands:
    """Data collection commands."""
    
    def create_group(self):
        """Create data command group."""
        
        @click.group(name='data')
        def data_group():
            """Data collection commands."""
            pass
        
        @data_group.command()
        @click.argument('device_id')
        @click.pass_context
        def collect(ctx, device_id: str):
            """Collect data from a specific device."""
            
            async def _collect():
                data_collection = ctx.obj['data_collection']
                
                try:
                    click.echo(f"Collecting data from device {device_id}...")
                    readings = await data_collection.collect_device_data(DeviceId(device_id))
                    
                    if not readings:
                        click.echo("No readings collected.")
                        return True
                    
                    click.echo(f"✅ Collected {len(readings)} readings")
                    
                    # Display readings
                    headers = ['Type', 'Value', 'Unit', 'Quality', 'Timestamp']
                    rows = []
                    
                    for reading in readings:
                        rows.append([
                            str(reading.reading_type),
                            f"{reading.value:.2f}" if isinstance(reading.value, float) else str(reading.value),
                            reading.unit,
                            reading.quality or 'good',
                            reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        ])
                    
                    click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
                    
                except Exception as e:
                    click.echo(f"❌ Error collecting data: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_collect())
            if not success:
                ctx.exit(1)
        
        @data_group.command()
        @click.pass_context
        def collect_all(ctx):
            """Collect data from all connected devices."""
            
            async def _collect_all():
                data_collection = ctx.obj['data_collection']
                
                try:
                    click.echo("Collecting data from all connected devices...")
                    results = await data_collection.collect_all_devices_data()
                    
                    if not results:
                        click.echo("No connected devices found.")
                        return True
                    
                    total_readings = sum(len(readings) for readings in results.values())
                    click.echo(f"✅ Collected {total_readings} readings from {len(results)} devices")
                    
                    # Display summary
                    headers = ['Device ID', 'Readings Count', 'Status']
                    rows = []
                    
                    for device_id, readings in results.items():
                        status = "✅ Success" if readings else "⚠️  No data"
                        rows.append([
                            str(device_id)[:8] + '...',
                            len(readings),
                            status
                        ])
                    
                    click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
                    
                except Exception as e:
                    click.echo(f"❌ Error collecting data: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_collect_all())
            if not success:
                ctx.exit(1)
        
        @data_group.command()
        @click.argument('device_id')
        @click.pass_context
        def latest(ctx, device_id: str):
            """Show latest readings for a device."""
            
            async def _latest():
                data_collection = ctx.obj['data_collection']
                
                try:
                    readings = await data_collection.get_latest_readings(DeviceId(device_id))
                    
                    if not readings:
                        click.echo("No readings found.")
                        return True
                    
                    click.echo(f"Latest readings for device {device_id}")
                    click.echo("=" * 50)
                    
                    # Display readings
                    headers = ['Type', 'Value', 'Unit', 'Quality', 'Timestamp']
                    rows = []
                    
                    for reading in readings:
                        rows.append([
                            str(reading.reading_type),
                            f"{reading.value:.2f}" if isinstance(reading.value, float) else str(reading.value),
                            reading.unit,
                            reading.quality or 'good',
                            reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        ])
                    
                    click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
                    
                except Exception as e:
                    click.echo(f"❌ Error getting latest readings: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_latest())
            if not success:
                ctx.exit(1)
        
        @data_group.command()
        @click.argument('device_id')
        @click.option('--hours', default=1, help='Hours of history to fetch')
        @click.option('--limit', default=100, help='Maximum number of readings')
        @click.pass_context
        def history(ctx, device_id: str, hours: int, limit: int):
            """Show historical readings for a device."""
            
            async def _history():
                data_collection = ctx.obj['data_collection']
                
                try:
                    start_time = datetime.utcnow() - timedelta(hours=hours)
                    readings = await data_collection.get_historical_readings(
                        DeviceId(device_id), 
                        start_time=start_time,
                        limit=limit
                    )
                    
                    if not readings:
                        click.echo(f"No readings found in the last {hours} hours.")
                        return True
                    
                    click.echo(f"Historical readings for device {device_id} (last {hours} hours)")
                    click.echo("=" * 70)
                    
                    # Display readings
                    headers = ['Type', 'Value', 'Unit', 'Quality', 'Timestamp']
                    rows = []
                    
                    for reading in readings[:limit]:  # Ensure we don't exceed limit
                        rows.append([
                            str(reading.reading_type),
                            f"{reading.value:.2f}" if isinstance(reading.value, float) else str(reading.value),
                            reading.unit,
                            reading.quality or 'good',
                            reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        ])
                    
                    click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
                    
                    if len(readings) >= limit:
                        click.echo(f"\n(Showing first {limit} readings)")
                    
                except Exception as e:
                    click.echo(f"❌ Error getting historical readings: {e}")
                    return False
                
                return True
            
            success = asyncio.run(_history())
            if not success:
                ctx.exit(1)
        
        return data_group