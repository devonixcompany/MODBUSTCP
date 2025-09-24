#!/usr/bin/env python3
"""Entry point for MODBUS TCP service CLI."""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    from presentation.cli.main import cli
    cli()