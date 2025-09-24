#!/usr/bin/env python3
"""API server entry point for MODBUS TCP service."""

import sys
import uvicorn
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    from presentation.api.main import app
    from infrastructure.config import load_config
    
    # Load configuration
    config = load_config()
    
    # Run the API server
    uvicorn.run(
        "presentation.api.main:app",
        host=config.api.host,
        port=config.api.port,
        workers=config.api.workers,
        reload=config.api.reload,
        log_level="info" if not config.debug else "debug"
    )