#!/usr/bin/env python3
"""
Development setup script for MODBUS TCP service.
Sets up the development environment with sample devices and configurations.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from domain.value_objects import DeviceId, DeviceType, ModbusAddress
from domain.entities import DeviceConfig, RegisterConfig
from infrastructure.database import (
    InMemoryDeviceRepository,
    InMemoryReadingRepository,
    InMemoryConfigRepository
)
from infrastructure.modbus import PyModbusClient
from application.use_cases import DeviceManagementUseCase


async def setup_sample_devices():
    """Setup sample devices for development."""
    
    # Initialize repositories and use case
    device_repo = InMemoryDeviceRepository()
    reading_repo = InMemoryReadingRepository()
    config_repo = InMemoryConfigRepository()
    modbus_client = PyModbusClient()
    
    device_mgmt = DeviceManagementUseCase(device_repo, config_repo, modbus_client)
    
    print("🚀 Setting up sample devices for development...")
    
    # Sample devices
    sample_devices = [
        {
            "name": "SDM120 Energy Meter",
            "type": DeviceType.sdm120(),
            "address": ModbusAddress("10.1.2.1", 502),
            "unit_id": 1
        },
        {
            "name": "PM2510-0D Dust Sensor", 
            "type": DeviceType.pm2510_0d(),
            "address": ModbusAddress("10.1.2.1", 502),
            "unit_id": 4
        },
        {
            "name": "XY-MD02 Environmental Sensor",
            "type": DeviceType.xy_md02(), 
            "address": ModbusAddress("10.1.2.1", 502),
            "unit_id": 2
        }
    ]
    
    devices_added = []
    
    for device_info in sample_devices:
        try:
            device = await device_mgmt.add_device(**device_info)
            devices_added.append(device)
            print(f"✅ Added device: {device.name} (ID: {device.id})")
            
            # Add sample configuration
            await setup_device_config(config_repo, device)
            
        except Exception as e:
            print(f"❌ Error adding device {device_info['name']}: {e}")
    
    if devices_added:
        print(f"\n🎉 Successfully added {len(devices_added)} sample devices!")
        print("\n📋 Available commands:")
        print("  modbustcp device list")
        print("  modbustcp test-connection --host 10.1.2.1 --unit 1")
        print("  modbustcp device connect <device-id>")
        print("  modbustcp data collect <device-id>")
        print("  modbustcp monitor health <device-id>")
    else:
        print("❌ No devices were added")


async def setup_device_config(config_repo, device):
    """Setup configuration for a device."""
    
    config = DeviceConfig(
        id=device.id,
        name=device.name,
        device_type=device.device_type,
        address=device.address,
        unit_id=device.unit_id,
        timeout=3,
        polling_interval=30
    )
    
    # Add registers based on device type
    if str(device.device_type) == "SDM120":
        config.registers = [
            RegisterConfig("voltage", 0x0000, "float32", "V", 1.0, 0.0, "Line voltage"),
            RegisterConfig("current", 0x0006, "float32", "A", 1.0, 0.0, "Current"),
            RegisterConfig("active_power", 0x000C, "float32", "W", 1.0, 0.0, "Active power"),
            RegisterConfig("frequency", 0x0046, "float32", "Hz", 1.0, 0.0, "Frequency"),
        ]
    elif str(device.device_type) == "PM2510-0D":
        config.registers = [
            RegisterConfig("pm25", 0x0004, "uint16", "µg/m³", 1.0, 0.0, "PM2.5 concentration"),
            RegisterConfig("pm10", 0x0009, "uint16", "µg/m³", 1.0, 0.0, "PM10 concentration"),
        ]
    elif str(device.device_type) == "XY-MD02":  
        config.registers = [
            RegisterConfig("temperature", 0x0001, "int16", "°C", 0.1, 0.0, "Temperature"),
            RegisterConfig("humidity", 0x0002, "uint16", "%RH", 0.1, 0.0, "Humidity"),
        ]
    
    await config_repo.save_config(config)


def create_directories():
    """Create necessary directories for development."""
    
    dirs_to_create = [
        "data",
        "logs", 
        "config/custom"
    ]
    
    base_path = Path(__file__).parent.parent
    
    for dir_name in dirs_to_create:
        dir_path = base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {dir_name}")


def main():
    """Main setup function."""
    
    print("🔧 MODBUS TCP Service - Development Setup")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Setup sample devices
    try:
        asyncio.run(setup_sample_devices())
    except KeyboardInterrupt:
        print("\n⚠️  Setup interrupted by user")
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)
    
    print("\n✨ Development environment setup complete!")
    print("🔗 Next steps:")
    print("  1. Test connectivity: modbustcp test-connection --host 10.1.2.1")
    print("  2. List devices: modbustcp device list") 
    print("  3. Check documentation: cat README.md")


if __name__ == "__main__":
    main()