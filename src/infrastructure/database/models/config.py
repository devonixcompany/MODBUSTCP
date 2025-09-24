"""Device configuration SQLAlchemy model."""

import sys
from pathlib import Path
from sqlalchemy import String, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from .base import Base, TimestampMixin


class DeviceConfigModel(Base, TimestampMixin):
    """SQLAlchemy model for DeviceConfig entity."""
    
    __tablename__ = "device_configs"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    device_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    device_type: Mapped[str] = mapped_column(String(50), nullable=False)
    host: Mapped[str] = mapped_column(String(255), nullable=False)
    port: Mapped[int] = mapped_column(Integer, default=502, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    timeout: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    registers: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    polling_interval: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    retry_count: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    metadata: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    def __repr__(self) -> str:
        return f"<DeviceConfigModel(device_id='{self.device_id}', name='{self.name}')>"