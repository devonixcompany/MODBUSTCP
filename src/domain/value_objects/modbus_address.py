"""MODBUS address value object."""

from dataclasses import dataclass
import ipaddress
from typing import Union


@dataclass(frozen=True)
class ModbusAddress:
    """MODBUS TCP address value object."""
    
    host: str
    port: int = 502
    
    def __post_init__(self):
        """Validate MODBUS address."""
        if not self.host or not self.host.strip():
            raise ValueError("Host cannot be empty")
        
        # Validate port range
        if not (1 <= self.port <= 65535):
            raise ValueError("Port must be between 1 and 65535")
        
        # Validate host format (IP address or hostname)
        host = self.host.strip()
        try:
            # Try to parse as IP address
            ipaddress.ip_address(host)
        except ValueError:
            # If not IP, validate as hostname (basic check)
            if not self._is_valid_hostname(host):
                raise ValueError(f"Invalid host format: {host}")
        
        # Set normalized values
        object.__setattr__(self, 'host', host)
    
    def _is_valid_hostname(self, hostname: str) -> bool:
        """Basic hostname validation."""
        if len(hostname) > 253:
            return False
        
        if hostname[-1] == ".":
            hostname = hostname[:-1]
        
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.")
        return (
            all(char in allowed for char in hostname) and
            not hostname.startswith('-') and
            not hostname.endswith('-') and
            '..' not in hostname
        )
    
    @classmethod
    def from_string(cls, address: str) -> 'ModbusAddress':
        """Create address from string format 'host:port' or 'host'."""
        parts = address.rsplit(':', 1)
        if len(parts) == 2:
            host, port_str = parts
            try:
                port = int(port_str)
            except ValueError:
                raise ValueError(f"Invalid port in address: {address}")
            return cls(host, port)
        else:
            return cls(parts[0])
    
    def to_tuple(self) -> tuple:
        """Convert to (host, port) tuple."""
        return (self.host, self.port)
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.host}:{self.port}"
    
    def __repr__(self) -> str:
        """Representation for debugging."""
        return f"ModbusAddress('{self.host}', {self.port})"