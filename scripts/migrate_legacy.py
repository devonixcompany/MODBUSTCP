#!/usr/bin/env python3
"""
Migration script to move legacy individual scripts to legacy folder.
This preserves the original scripts while promoting the new clean architecture.
"""

import os
import shutil
from pathlib import Path


def migrate_legacy_scripts():
    """Move legacy scripts to a legacy folder."""
    
    # Get current directory
    current_dir = Path(__file__).parent.parent
    
    # Create legacy directory
    legacy_dir = current_dir / "legacy"
    legacy_dir.mkdir(exist_ok=True)
    
    # Legacy scripts to move
    legacy_scripts = [
        "sdm120_read.py",
        "pm2510_0d_summary.py", 
        "xy_md02_summary.py"
    ]
    
    moved_files = []
    
    for script in legacy_scripts:
        script_path = current_dir / script
        if script_path.exists():
            target_path = legacy_dir / script
            shutil.move(str(script_path), str(target_path))
            moved_files.append(script)
            print(f"✅ Moved {script} to legacy/")
    
    if moved_files:
        # Create README in legacy folder
        readme_content = """# Legacy Scripts

These are the original individual MODBUS device scripts that have been replaced by the new clean architecture implementation.

## Replaced Scripts

- `sdm120_read.py` → Use `modbustcp device add --type SDM120` + `modbustcp data collect`
- `pm2510_0d_summary.py` → Use `modbustcp device add --type PM2510-0D` + `modbustcp data collect`
- `xy_md02_summary.py` → Use `modbustcp device add --type XY-MD02` + `modbustcp data collect`

## Migration

The new architecture provides the same functionality with improved:
- Error handling and logging
- Configuration management  
- Monitoring and health checks
- Production readiness
- Docker support

## Usage with New System

1. Add device:
```bash
modbustcp device add --name "Energy Meter" --type SDM120 --host 10.1.2.1 --unit 1
```

2. Collect data:
```bash
modbustcp data collect <device-id>
```

3. Monitor device:
```bash
modbustcp monitor health <device-id>
```

See main README.md for complete documentation.
"""
        
        with open(legacy_dir / "README.md", "w") as f:
            f.write(readme_content)
        
        print(f"\n✅ Created legacy/README.md with migration instructions")
        print(f"\n🎉 Successfully migrated {len(moved_files)} legacy scripts")
        print("💡 The new clean architecture implementation is now ready to use!")
        print("📖 See README.md for usage instructions")
    else:
        print("ℹ️  No legacy scripts found to migrate")


if __name__ == "__main__":
    migrate_legacy_scripts()