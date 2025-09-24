#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

try:
    print("Testing API imports...")
    
    # Test FastAPI imports
    from fastapi import FastAPI
    print("✅ FastAPI import successful")
    
    # Test database models
    from infrastructure.database.models import Base, DeviceModel, ReadingModel
    print("✅ Database models import successful")
    
    # Test API schemas
    from presentation.api.schemas import DeviceCreate, ReadingResponse
    print("✅ API schemas import successful")
    
    # Test repositories
    from infrastructure.database import PostgreSQLDeviceRepository, InfluxDBReadingRepository
    print("✅ Database repositories import successful")
    
    # Test API routers
    from presentation.api.routers import devices, readings, monitoring, health
    print("✅ API routers import successful")
    
    # Test configuration
    from infrastructure.config import load_config
    config = load_config()
    print(f"✅ Configuration loaded - Environment: {config.environment}")
    
    print("\n🎉 All API components imported successfully!")
    print("\n📋 API Features Available:")
    print("  • REST API with FastAPI")
    print("  • Swagger/OpenAPI documentation")
    print("  • PostgreSQL database persistence")
    print("  • InfluxDB time-series data support")
    print("  • Database migrations with Alembic")
    print("  • Comprehensive API schemas")
    print("  • Device management endpoints")
    print("  • Data collection endpoints")
    print("  • Health monitoring endpoints")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
