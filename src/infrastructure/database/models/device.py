"""Device SQLAlchemy model."""

import sys
from pathlib import Path
from sqlalchemy import String, Integer, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from domain.entities.device import DeviceStatus
from .base import Base, TimestampMixin


class DeviceModel(Base, TimestampMixin):
    """SQLAlchemy model for Device entity."""
    
    __tablename__ = "devices"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    device_type: Mapped[str] = mapped_column(String(50), nullable=False)
    host: Mapped[str] = mapped_column(String(255), nullable=False)
    port: Mapped[int] = mapped_column(Integer, default=502, nullable=False)
    unit_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[DeviceStatus] = mapped_column(
        SQLEnum(DeviceStatus),
        default=DeviceStatus.DISCONNECTED,
        nullable=False
    )
    metadata: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    def __repr__(self) -> str:
        return f"<DeviceModel(id='{self.id}', name='{self.name}', type='{self.device_type}')>"