"""FastAPI application factory."""

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from infrastructure.config import load_config
from infrastructure.database import (
    PostgreSQLDeviceRepository,
    PostgreSQLReadingRepository,
    PostgreSQLConfigRepository,
    InfluxDBReadingRepository,
)
from infrastructure.modbus import PyModbusClient
from application.use_cases import (
    DeviceManagementUseCase,
    DataCollectionUseCase,
    DeviceMonitoringUseCase,
)
from .routers import devices, readings, monitoring, health
from .middleware.error_handler import ErrorHandlerMiddleware


def create_app(config_path: str = None) -> FastAPI:
    """Create and configure FastAPI application."""
    
    # Load configuration
    config = load_config(config_path)
    
    # Create FastAPI app
    app = FastAPI(
        title="MODBUS TCP Service API",
        description="Production-ready MODBUS TCP service with REST API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add custom error handling middleware
    app.add_middleware(ErrorHandlerMiddleware)
    
    # Initialize dependencies
    # Database repositories
    device_repo = PostgreSQLDeviceRepository(config.database.connection_string)
    config_repo = PostgreSQLConfigRepository(config.database.connection_string)
    
    # Choose reading repository based on configuration
    if config.database.reading_store == "influxdb":
        reading_repo = InfluxDBReadingRepository(
            config.influxdb.url,
            config.influxdb.token,
            config.influxdb.org,
            config.influxdb.bucket
        )
    else:
        reading_repo = PostgreSQLReadingRepository(config.database.connection_string)
    
    # MODBUS client
    modbus_client = PyModbusClient()
    
    # Use cases
    device_mgmt = DeviceManagementUseCase(device_repo, config_repo, modbus_client)
    data_collection = DataCollectionUseCase(device_repo, reading_repo, config_repo, modbus_client)
    monitoring = DeviceMonitoringUseCase(device_repo, reading_repo, data_collection, modbus_client)
    
    # Store dependencies in app state
    app.state.config = config
    app.state.device_mgmt = device_mgmt
    app.state.data_collection = data_collection
    app.state.monitoring = monitoring
    
    # Include routers
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(devices.router, prefix="/api/v1", tags=["Devices"])
    app.include_router(readings.router, prefix="/api/v1", tags=["Readings"])
    app.include_router(monitoring.router, prefix="/api/v1", tags=["Monitoring"])
    
    return app


# Create app instance for running with uvicorn
app = create_app()