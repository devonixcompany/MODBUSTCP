"""Health check router."""

import sys
from pathlib import Path
from fastapi import APIRouter, Request
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

router = APIRouter()


@router.get("/health", response_model=Dict[str, Any])
async def health_check(request: Request) -> Dict[str, Any]:
    """API health check endpoint."""
    return {
        "status": "healthy",
        "service": "MODBUS TCP Service API",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }


@router.get("/", response_model=Dict[str, Any])
async def root(request: Request) -> Dict[str, Any]:
    """Root endpoint with API information."""
    return {
        "service": "MODBUS TCP Service API",
        "version": "1.0.0",
        "description": "Production-ready MODBUS TCP service with REST API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "health_url": "/api/v1/health"
    }