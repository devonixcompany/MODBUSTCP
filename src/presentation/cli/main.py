"""Main CLI interface for MODBUS TCP service."""

import asyncio
import logging
import sys
from typing import Optional
from pathlib import Path

import click

# Add src to path for standalone execution
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from infrastructure.config import load_config
from infrastructure.database import (
    InMemoryDeviceRepository,
    InMemoryReadingRepository,
    InMemoryConfigRepository
)
from infrastructure.modbus import PyModbusClient
from application.use_cases import (
    DeviceManagementUseCase,
    DataCollectionUseCase,
    DeviceMonitoringUseCase
)
from .commands import DeviceCommands, DataCommands, MonitoringCommands


def setup_logging(config):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, config.logging.level.upper()),
        format=config.logging.format,
        filename=config.logging.file
    )


def create_use_cases():
    """Create and wire up use cases with dependencies."""
    # Infrastructure
    device_repo = InMemoryDeviceRepository()
    reading_repo = InMemoryReadingRepository()
    config_repo = InMemoryConfigRepository()
    modbus_client = PyModbusClient()
    
    # Use cases
    device_mgmt = DeviceManagementUseCase(device_repo, config_repo, modbus_client)
    data_collection = DataCollectionUseCase(device_repo, reading_repo, config_repo, modbus_client)
    monitoring = DeviceMonitoringUseCase(device_repo, reading_repo, data_collection, modbus_client)
    
    return device_mgmt, data_collection, monitoring


@click.group()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.pass_context
def cli(ctx, config: Optional[str], debug: bool):
    """MODBUS TCP Service - Clean Architecture Implementation."""
    
    # Load configuration
    app_config = load_config(config)
    if debug:
        app_config.debug = True
        app_config.logging.level = "DEBUG"
    
    # Setup logging
    setup_logging(app_config)
    
    # Create use cases
    device_mgmt, data_collection, monitoring = create_use_cases()
    
    # Store in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj['config'] = app_config
    ctx.obj['device_mgmt'] = device_mgmt
    ctx.obj['data_collection'] = data_collection
    ctx.obj['monitoring'] = monitoring


# Add command groups
cli.add_command(DeviceCommands().create_group())
cli.add_command(DataCommands().create_group())
cli.add_command(MonitoringCommands().create_group())


@cli.command()
@click.pass_context
def info(ctx):
    """Show application information."""
    config = ctx.obj['config']
    
    click.echo("MODBUS TCP Service")
    click.echo("=" * 50)
    click.echo(f"Environment: {config.environment}")
    click.echo(f"Debug: {config.debug}")
    click.echo(f"Log Level: {config.logging.level}")
    click.echo(f"MODBUS Timeout: {config.modbus.default_timeout}s")
    click.echo(f"Poll Interval: {config.monitoring.default_poll_interval}s")


@cli.command()
@click.option('--host', default='10.1.2.1', help='MODBUS host address')
@click.option('--port', default=502, help='MODBUS port')
@click.option('--unit', default=1, help='MODBUS unit ID')
@click.option('--timeout', default=3, help='Connection timeout')
@click.pass_context
def test_connection(ctx, host: str, port: int, unit: int, timeout: int):
    """Test connection to a MODBUS device."""
    
    async def _test():
        from domain.value_objects import ModbusAddress
        from infrastructure.modbus import PyModbusClient
        
        client = PyModbusClient()
        address = ModbusAddress(host, port)
        
        click.echo(f"Testing connection to {address} (unit {unit})...")
        
        try:
            success = await client.connect(address, unit, timeout)
            if success:
                click.echo(f"✅ Successfully connected to {address}")
                
                # Try reading a register
                registers = await client.read_input_registers(0, 1)
                if registers:
                    click.echo(f"✅ Successfully read test register: {registers[0]}")
                else:
                    click.echo("⚠️  Connected but could not read test register")
                
                await client.disconnect()
                click.echo("✅ Disconnected successfully")
            else:
                click.echo(f"❌ Failed to connect to {address}")
                return False
                
        except Exception as e:
            click.echo(f"❌ Connection error: {e}")
            return False
        
        return True
    
    success = asyncio.run(_test())
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    cli()