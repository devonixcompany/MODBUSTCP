"""MODBUS client interface."""

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from ...domain.value_objects import ModbusAddress


class ModbusClient(ABC):
    """Abstract MODBUS TCP client interface."""
    
    @abstractmethod
    async def connect(self, address: ModbusAddress, unit_id: int, timeout: int = 3) -> bool:
        """Connect to MODBUS device."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from MODBUS device."""
        pass
    
    @abstractmethod
    async def is_connected(self) -> bool:
        """Check if connected to device."""
        pass
    
    @abstractmethod
    async def read_holding_registers(
        self, 
        address: int, 
        count: int = 1
    ) -> Optional[List[int]]:
        """Read holding registers (function code 03)."""
        pass
    
    @abstractmethod
    async def read_input_registers(
        self, 
        address: int, 
        count: int = 1
    ) -> Optional[List[int]]:
        """Read input registers (function code 04)."""
        pass
    
    @abstractmethod
    async def read_coils(
        self, 
        address: int, 
        count: int = 1
    ) -> Optional[List[bool]]:
        """Read coils (function code 01)."""
        pass
    
    @abstractmethod
    async def read_discrete_inputs(
        self, 
        address: int, 
        count: int = 1
    ) -> Optional[List[bool]]:
        """Read discrete inputs (function code 02)."""
        pass
    
    @abstractmethod
    async def write_single_register(
        self, 
        address: int, 
        value: int
    ) -> bool:
        """Write single register (function code 06)."""
        pass
    
    @abstractmethod
    async def write_multiple_registers(
        self, 
        address: int, 
        values: List[int]
    ) -> bool:
        """Write multiple registers (function code 16)."""
        pass
    
    @abstractmethod
    async def read_float32(
        self, 
        address: int, 
        byte_order: str = "big"
    ) -> Optional[float]:
        """Read 32-bit float from two consecutive registers."""
        pass
    
    @abstractmethod
    async def read_int16(self, address: int, signed: bool = True) -> Optional[int]:
        """Read 16-bit integer from register."""
        pass