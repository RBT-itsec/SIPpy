"""
Common objects used by plugins
"""

from dataclasses import dataclass
from typing import Optional
from ipaddress import IPv4Address, IPv6Address


@dataclass
class NetworkInterfaceState():
    """ Represents a network interface's state """
    isup: bool
    speed: int
    mtu: int


@dataclass
class NetworkInterfaceAddrs():
    """ Represents a network interface's addresses """
    # ethernet: str  # fails on windows pseudo-interface
    ipv4: IPv4Address
    ipv4mask: IPv4Address
    ipv6: Optional[IPv6Address] = None
    ipv6mask: Optional[IPv6Address] = None


@dataclass
class NetworkInterface():
    """ Represents a network interface """
    name: str
    state: NetworkInterfaceState
    addrs: NetworkInterfaceAddrs
