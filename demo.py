#!/usr/bin/env python3
"""
Demo script showcasing the new MODBUS TCP Clean Architecture implementation.
This replaces the individual legacy scripts with a unified, production-ready solution.
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from domain.value_objects import DeviceId, DeviceType, ModbusAddress
from domain.entities import Device, Reading, DeviceConfig
from domain.entities.device_config import RegisterConfig
from infrastructure.database import (
    InMemoryDeviceRepository,
    InMemoryReadingRepository,
    InMemoryConfigRepository
)
from application.use_cases import DeviceManagementUseCase
from datetime import datetime


async def demo_clean_architecture():
    """Demonstrate the clean architecture implementation."""
    
    print("🏗️  MODBUS TCP Clean Architecture Demo")
    print("=" * 60)
    
    # Initialize the clean architecture layers
    print("📦 Initializing clean architecture components...")
    
    # Infrastructure Layer (Repositories)
    device_repo = InMemoryDeviceRepository()
    reading_repo = InMemoryReadingRepository()
    config_repo = InMemoryConfigRepository()
    
    # Application Layer (Use Cases) 
    device_mgmt = DeviceManagementUseCase(device_repo, config_repo, None)
    
    print("✅ Infrastructure and application layers initialized")
    
    # Domain Layer Demo
    print("\n🎯 Domain Layer Demo:")
    
    # Create Value Objects
    device_id = DeviceId.generate()
    sdm120_type = DeviceType.sdm120()
    pm2510_type = DeviceType.pm2510_0d()
    xy_md02_type = DeviceType.xy_md02()
    address = ModbusAddress("10.1.2.1", 502)
    
    print(f"  📋 Generated Device ID: {device_id}")
    print(f"  ⚡ SDM120 Type: {sdm120_type}")
    print(f"  🌫️  PM2510-0D Type: {pm2510_type}")
    print(f"  🌡️  XY-MD02 Type: {xy_md02_type}")
    print(f"  🌐 MODBUS Address: {address}")
    
    # Create Entities
    devices = [
        Device(
            id=DeviceId.generate(),
            name="Main Energy Meter",
            device_type=sdm120_type,
            address=address,
            unit_id=1
        ),
        Device(
            id=DeviceId.generate(),
            name="Air Quality Sensor",
            device_type=pm2510_type,
            address=address,
            unit_id=4
        ),
        Device(
            id=DeviceId.generate(),
            name="Environmental Sensor",
            device_type=xy_md02_type,
            address=address,
            unit_id=2
        )
    ]
    
    # Application Layer Demo
    print("\n🚀 Application Layer Demo:")
    
    for device in devices:
        await device_mgmt.add_device(
            device.name,
            device.device_type,
            device.address,
            device.unit_id,
            device.id
        )
        print(f"  ✅ Added {device.name} ({device.device_type})")
    
    # List all devices
    all_devices = await device_mgmt.list_devices()
    print(f"\n📊 Total devices managed: {len(all_devices)}")
    
    # Create sample configurations
    print("\n⚙️  Configuration Management Demo:")
    
    for device in all_devices:
        config = DeviceConfig(
            id=device.id,
            name=device.name,
            device_type=device.device_type,
            address=device.address,
            unit_id=device.unit_id,
            timeout=3,
            polling_interval=30
        )
        
        # Add sample registers based on device type
        if str(device.device_type) == "SDM120":
            config.registers = [
                RegisterConfig("voltage", 0x0000, "float32", "V", 1.0, 0.0, "Voltage"),
                RegisterConfig("current", 0x0006, "float32", "A", 1.0, 0.0, "Current"),
                RegisterConfig("power", 0x000C, "float32", "W", 1.0, 0.0, "Active Power"),
            ]
        elif str(device.device_type) == "PM2510-0D":
            config.registers = [
                RegisterConfig("pm25", 0x0004, "uint16", "µg/m³", 1.0, 0.0, "PM2.5"),
                RegisterConfig("pm10", 0x0009, "uint16", "µg/m³", 1.0, 0.0, "PM10"),
            ]
        elif str(device.device_type) == "XY-MD02":
            config.registers = [
                RegisterConfig("temperature", 0x0001, "int16", "°C", 0.1, 0.0, "Temperature"),
                RegisterConfig("humidity", 0x0002, "uint16", "%RH", 0.1, 0.0, "Humidity"),
            ]
        
        await config_repo.save_config(config)
        print(f"  📝 Configured {device.name} with {len(config.registers)} registers")
    
    # Create sample readings
    print("\n📈 Data Management Demo:")
    
    for device in all_devices:
        # Simulate readings based on device type
        if str(device.device_type) == "SDM120":
            readings = [
                Reading(device.id, "voltage", 230.5, "V", datetime.utcnow(), 0x0000, "good"),
                Reading(device.id, "current", 12.3, "A", datetime.utcnow(), 0x0006, "good"),
                Reading(device.id, "power", 2835.0, "W", datetime.utcnow(), 0x000C, "good"),
            ]
        elif str(device.device_type) == "PM2510-0D":
            readings = [
                Reading(device.id, "pm25", 35, "µg/m³", datetime.utcnow(), 0x0004, "good"),
                Reading(device.id, "pm10", 55, "µg/m³", datetime.utcnow(), 0x0009, "good"),
            ]
        elif str(device.device_type) == "XY-MD02":
            readings = [
                Reading(device.id, "temperature", 23.5, "°C", datetime.utcnow(), 0x0001, "good"),
                Reading(device.id, "humidity", 65.2, "%RH", datetime.utcnow(), 0x0002, "good"),
            ]
        
        await reading_repo.save_batch(readings)
        print(f"  📊 Stored {len(readings)} readings for {device.name}")
    
    # Show architecture benefits
    print("\n🏆 Clean Architecture Benefits:")
    print("  ✅ Separation of Concerns - Domain, Application, Infrastructure")
    print("  ✅ Testable - Each layer can be tested independently")
    print("  ✅ Maintainable - Clear boundaries and responsibilities")
    print("  ✅ Scalable - Easy to add new devices and features")
    print("  ✅ Production Ready - Proper error handling, logging, monitoring")
    print("  ✅ Docker Support - Containerized deployment")
    
    # Show migration from legacy
    print("\n🔄 Migration from Legacy Scripts:")
    print("  📜 sdm120_read.py → SDM120 device configuration + unified CLI")
    print("  📜 pm2510_0d_summary.py → PM2510-0D device configuration + unified CLI")
    print("  📜 xy_md02_summary.py → XY-MD02 device configuration + unified CLI")
    
    print("\n🎯 Next Steps:")
    print("  1. Configure your devices using config/devices/*.yaml")
    print("  2. Use Docker: docker-compose up -d")
    print("  3. CLI Commands:")
    print("     • python modbustcp.py device list")
    print("     • python modbustcp.py test-connection --host 10.1.2.1 --unit 1")
    print("     • python modbustcp.py device add --name 'Meter' --type SDM120 --host 10.1.2.1 --unit 1")
    print("     • python modbustcp.py data collect <device-id>")
    print("     • python modbustcp.py monitor health <device-id>")
    
    print("\n✨ Clean Architecture Implementation Complete!")


if __name__ == "__main__":
    print("Starting MODBUS TCP Clean Architecture Demo...")
    try:
        asyncio.run(demo_clean_architecture())
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()