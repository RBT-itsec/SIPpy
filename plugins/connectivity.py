"""
Basic tests for network connectivity

Each exported plugin needs to accept the target system as _one_ parameter.
"""
# pylint: disable=W1203

import subprocess
import re
import socket
import logging

from typing import Dict, Optional

from . import register_plugin, Plugin

LOGGER = logging.getLogger("SIPpy.Connectivity")

GW_MATCH = re.compile(r'via (([0-9]{1,3}\.){3}[0-9]{1,3})')
IF_MATCH = re.compile(r'dev ([a-z0-9]+)\s')

# add plugin for changing local network configuration


@register_plugin
class BaseCheck(Plugin):
    name: str = "base_check"
    category: str = "connectivity"
    config: Dict = {}
    output: Dict = {}

    def _run(self, target: str):
        self.base_check(target)

    def base_check(self, target: str) -> Dict:
        """ Do some basic checks (route, link, ...) """
        _gwcheck = self._gateway(target)
        _gw = _gwcheck.get('gateway')
        _dev = _gwcheck.get('interface')
        _gw_reachable: bool = False

        if not _dev:
            _dev = "unknown"
            _dev_flags = self._interface_state("null")
        else:
            _dev_flags = self._interface_state(_dev)

        if _gw and _gw != "link-local" and _dev_flags['operstate'] == "up":
            _gw_reachable = True if Ping().ping(_gw) else False
        if _gw == "link-local":
            _gw_reachable = True
        return {'gateway': _gw, 'reachable': _gw_reachable,
                'dev': _dev, 'flags': _dev_flags}

    def _gateway(self, target: str) -> Dict:
        """ Get gateway to address """
        _gateway: Optional[str] = None
        _interface: Optional[str] = None

        try:
            completed = subprocess.run(
                ["ip", "route", "get", target], capture_output=True)

            if not completed.returncode:
                route = completed.stdout.splitlines()[0].decode()
                if "via" in route:
                    # Search for gateway
                    _gwmatch = GW_MATCH.search(route)
                    if _gwmatch and _gwmatch.group(1):
                        _gateway = _gwmatch.group(1)
                    else:
                        _gateway = None
                else:
                    _gateway = "link-local"

                # Search for interface name
                _ifmatch = IF_MATCH.search(route)
                if _ifmatch and _ifmatch.group(1):
                    _interface = _ifmatch.group(1)
                else:
                    _interface = None
            else:
                LOGGER.critical(
                    f"Route command failed with code {completed.returncode}")
        except FileNotFoundError:
            LOGGER.critical(f"IProute2 program not found")

        return {'gateway': _gateway, 'interface': _interface}

    def _interface_state(self, interface: str) -> Dict[str, Optional[str]]:
        """ Get interface state """
        flags: Dict[str, Optional[str]] = {
            'speed': None, 'operstate': None, 'duplex': None}

        if interface == "null":
            return flags

        _basepath = f"/sys/class/net/{interface}/"

        if interface:
            for flag in flags:
                try:
                    with open(f"{_basepath}{flag}") as infile:
                        flags[flag] = infile.read().strip()
                except FileNotFoundError:
                    LOGGER.warning(f"File {_basepath}{flag} not found")
        else:
            LOGGER.warning(f"No interface given for interface status check")

        return flags


@register_plugin
class Ping(Plugin):
    name: str = "ping"
    category: str = "connectivity"
    config: Dict = {}
    output: Dict = {}

    def _run(self, target: str):
        return self.ping(target)

    def ping(self, target: str) -> Dict[str, Optional[str]]:
        """ Run the ping command """
        rtts: Dict[str, Optional[str]] = {
            'min': None, 'avg': None, 'max': None}

        try:
            completed = subprocess.run(
                ['ping', '-c', '3', target], capture_output=True)

            if not completed.returncode:
                _rtts = completed.stdout.splitlines()[-1].decode()
                _rtts = _rtts.split(" ")[3].split("/")
                rtts['min'] = _rtts[0]
                rtts['avg'] = _rtts[1]
                rtts['max'] = _rtts[2]
        except FileNotFoundError:
            LOGGER.critical(f"Ping program not found")

        return rtts


# @register_plugin("connectivity")
# # TODO: accept more than one arg in plugins
# def tcp_port_5060(target: str) -> Dict:
#     """ Check if TCP port is reachable """
#     # TODO: Test it!
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.settimeout(3)  # TODO: read from config
#     connect = 1
#     try:
#         connect = sock.connect_ex((target, 5060))  # return 0 if successfull
#     except socket.gaierror:
#         LOGGER.warning(f"Unable to resolve address of {target}")
#     finally:
#         sock.close()

#     result = {'connect': True if not connect else False}
#     return result
