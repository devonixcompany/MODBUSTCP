"""Reading SQLAlchemy model."""

import sys
from pathlib import Path
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from .base import Base


class ReadingModel(Base):
    """SQLAlchemy model for Reading entity."""
    
    __tablename__ = "readings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_id: Mapped[str] = mapped_column(
        String(36), 
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    reading_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    register_address: Mapped[int] = mapped_column(Integer, nullable=False)
    quality: Mapped[str] = mapped_column(String(20), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, nullable=True)
    
    # Create composite indexes for common queries
    __table_args__ = (
        Index('ix_readings_device_timestamp', 'device_id', 'timestamp'),
        Index('ix_readings_device_type', 'device_id', 'reading_type'),
        Index('ix_readings_timestamp_desc', 'timestamp', postgresql_using='btree'),
    )
    
    def __repr__(self) -> str:
        return f"<ReadingModel(device_id='{self.device_id}', type='{self.reading_type}', value={self.value})>"