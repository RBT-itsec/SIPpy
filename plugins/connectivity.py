"""
Basic tests for network connectivity
"""

import subprocess
# import socket
from ipaddress import IPv4Address, IPv6Address
import re

from typing import List, Dict

from . import register_plugin
# from .objects import NetworkInterface, NetworkInterfaceState, NetworkInterfaceAddrs

GW_MATCH = re.compile(r'via (([0-9]{1,3}\.){3}[0-9]{1,3})')
IF_MATCH = re.compile(r'dev ([a-z0-9]+)\s')


@register_plugin
def base_check(target: str):
    """ Do some basic checks (route, link, ...) """
    _gw = _gateway(target)
    if _gw:
        _gw, _dev = _gw  # unpack gateway and device
        _dev_flags = _interface_state(_dev)
        # return gateway, interface and interface flags
        return (_gw, _dev, _dev_flags)
    else:
        return False


def _gateway(target: str) -> str:
    """ Get gateway to address """
    completed = subprocess.run(
        ["ip", "route", "get", target], capture_output=True)
    if not completed.returncode:
        route = completed.stdout.splitlines()[0].decode()
        if "via" in route:
            # Search for gateway
            _gateway = GW_MATCH.search(route)
            if _gateway:
                _gateway = _gateway.group(1)
            else:
                return False
        else:
            _gateway = "local link"

        # Search for interface name
        _interface = IF_MATCH.search(route)
        if _interface:
            _interface = _interface.group(1)
        else:
            return False
    else:
        return False

    return (_gateway, _interface)


def _interface_state(interface: str):
    """ Get interface state """
    _basepath = f"/sys/class/net/{interface}/"

    flags = {'speed': None, 'operstate': None, 'duplex': None}

    for flag in flags:
        try:
            with open(f"{_basepath}{flag}") as infile:
                flags[flag] = infile.read().strip()
        except FileNotFoundError:
            print(f"File {_basepath}{flag} not found")

    return flags


@register_plugin
def ping(target: str) -> bool:
    """ Run the ping command """
    completed = subprocess.run(
        ['ping', '-c', '3', target], capture_output=True)

    if not completed.returncode:
        _rtts = completed.stdout.splitlines()[-1].decode()
        _rtts = _rtts.split(" ")[3].split("/")
        rtts = {}
        rtts['min'] = _rtts[0]
        rtts['avg'] = _rtts[1]
        rtts['max'] = _rtts[2]
    else:
        rtts = False
    
    return rtts
