"""PyModbus client implementation."""

from typing import List, Optional
import logging
import asyncio

from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

from ...application.interfaces import ModbusClient
from ...domain.value_objects import ModbusAddress

logger = logging.getLogger(__name__)


class PyModbusClient(ModbusClient):
    """PyModbus implementation of MODBUS TCP client."""
    
    def __init__(self):
        self._client: Optional[ModbusTcpClient] = None
        self._current_address: Optional[ModbusAddress] = None
        self._current_unit_id: Optional[int] = None
        self._lock = asyncio.Lock()
    
    async def connect(self, address: ModbusAddress, unit_id: int, timeout: int = 3) -> bool:
        """Connect to MODBUS device."""
        async with self._lock:
            try:
                # Close existing connection if any
                if self._client:
                    await self.disconnect()
                
                self._client = ModbusTcpClient(
                    host=address.host,
                    port=address.port,
                    timeout=timeout
                )
                
                # Connect in thread pool to avoid blocking
                loop = asyncio.get_event_loop()
                connected = await loop.run_in_executor(None, self._client.connect)
                
                if connected:
                    self._current_address = address
                    self._current_unit_id = unit_id
                    logger.info(f"Connected to MODBUS device at {address}")
                    return True
                else:
                    logger.error(f"Failed to connect to MODBUS device at {address}")
                    self._client = None
                    return False
                    
            except Exception as e:
                logger.error(f"Error connecting to MODBUS device at {address}: {e}")
                self._client = None
                return False
    
    async def disconnect(self) -> None:
        """Disconnect from MODBUS device."""
        async with self._lock:
            if self._client:
                try:
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, self._client.close)
                    logger.info(f"Disconnected from MODBUS device at {self._current_address}")
                except Exception as e:
                    logger.error(f"Error disconnecting from MODBUS device: {e}")
                finally:
                    self._client = None
                    self._current_address = None
                    self._current_unit_id = None
    
    async def is_connected(self) -> bool:
        """Check if connected to device."""
        return self._client is not None and self._client.is_socket_open()
    
    async def read_holding_registers(self, address: int, count: int = 1) -> Optional[List[int]]:
        """Read holding registers (function code 03)."""
        if not self._client or self._current_unit_id is None:
            return None
        
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._client.read_holding_registers,
                address,
                count,
                self._current_unit_id
            )
            
            if result.isError():
                logger.error(f"Error reading holding registers at {address}: {result}")
                return None
            
            return result.registers
            
        except Exception as e:
            logger.error(f"Exception reading holding registers at {address}: {e}")
            return None
    
    async def read_input_registers(self, address: int, count: int = 1) -> Optional[List[int]]:
        """Read input registers (function code 04)."""
        if not self._client or self._current_unit_id is None:
            return None
        
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._client.read_input_registers,
                address,
                count,
                self._current_unit_id
            )
            
            if result.isError():
                logger.error(f"Error reading input registers at {address}: {result}")
                return None
            
            return result.registers
            
        except Exception as e:
            logger.error(f"Exception reading input registers at {address}: {e}")
            return None
    
    async def read_coils(self, address: int, count: int = 1) -> Optional[List[bool]]:
        """Read coils (function code 01)."""
        if not self._client or self._current_unit_id is None:
            return None
        
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._client.read_coils,
                address,
                count,
                self._current_unit_id
            )
            
            if result.isError():
                logger.error(f"Error reading coils at {address}: {result}")
                return None
            
            return result.bits
            
        except Exception as e:
            logger.error(f"Exception reading coils at {address}: {e}")
            return None
    
    async def read_discrete_inputs(self, address: int, count: int = 1) -> Optional[List[bool]]:
        """Read discrete inputs (function code 02)."""
        if not self._client or self._current_unit_id is None:
            return None
        
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._client.read_discrete_inputs,
                address,
                count,
                self._current_unit_id
            )
            
            if result.isError():
                logger.error(f"Error reading discrete inputs at {address}: {result}")
                return None
            
            return result.bits
            
        except Exception as e:
            logger.error(f"Exception reading discrete inputs at {address}: {e}")
            return None
    
    async def write_single_register(self, address: int, value: int) -> bool:
        """Write single register (function code 06)."""
        if not self._client or self._current_unit_id is None:
            return False
        
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._client.write_register,
                address,
                value,
                self._current_unit_id
            )
            
            if result.isError():
                logger.error(f"Error writing register at {address}: {result}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Exception writing register at {address}: {e}")
            return False
    
    async def write_multiple_registers(self, address: int, values: List[int]) -> bool:
        """Write multiple registers (function code 16)."""
        if not self._client or self._current_unit_id is None:
            return False
        
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._client.write_registers,
                address,
                values,
                self._current_unit_id
            )
            
            if result.isError():
                logger.error(f"Error writing registers at {address}: {result}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Exception writing registers at {address}: {e}")
            return False
    
    async def read_float32(self, address: int, byte_order: str = "big") -> Optional[float]:
        """Read 32-bit float from two consecutive registers."""
        registers = await self.read_input_registers(address, 2)
        if not registers or len(registers) != 2:
            return None
        
        try:
            # Handle different endianness
            if byte_order.lower() == "big":
                byteorder = Endian.BIG
                wordorder = Endian.BIG
            else:
                byteorder = Endian.LITTLE
                wordorder = Endian.LITTLE
            
            decoder = BinaryPayloadDecoder.fromRegisters(
                registers, 
                byteorder=byteorder, 
                wordorder=wordorder
            )
            return decoder.decode_32bit_float()
            
        except Exception as e:
            logger.error(f"Error decoding float32 from registers: {e}")
            return None
    
    async def read_int16(self, address: int, signed: bool = True) -> Optional[int]:
        """Read 16-bit integer from register."""
        registers = await self.read_input_registers(address, 1)
        if not registers:
            return None
        
        value = registers[0]
        
        # Convert to signed if requested
        if signed and value >= 0x8000:
            value = value - 0x10000
        
        return value