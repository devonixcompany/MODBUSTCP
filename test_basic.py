#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

# Test basic imports
try:
    from domain.value_objects import DeviceId, DeviceType, ModbusAddress
    print("✅ Domain imports successful")
    
    # Test value objects
    device_id = DeviceId.generate()
    device_type = DeviceType.sdm120()
    address = ModbusAddress("10.1.2.1", 502)
    
    print(f"✅ DeviceId: {device_id}")
    print(f"✅ DeviceType: {device_type}")
    print(f"✅ Address: {address}")
    
    from infrastructure.modbus import PyModbusClient
    print("✅ Infrastructure imports successful")
    
    print("\n🎉 Basic functionality test passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
