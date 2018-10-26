"""
Basic tests for network connectivity

Each exported plugin needs to accept the target system as _one_ parameter.
"""
# pylint: disable=W1203

import subprocess
import re
import logging

from typing import Dict, Optional, Tuple

from lib.objects import Testcase
from . import register_plugin

LOGGER = logging.getLogger("SIPpy.Connectivity")

GW_MATCH = re.compile(r'via (([0-9]{1,3}\.){3}[0-9]{1,3})')
IF_MATCH = re.compile(r'dev ([a-z0-9]+)\s')


@register_plugin
# def base_check(target: str) -> Tuple[Optional[str], bool, Optional[str], Dict[str, Optional[str]]]:
def base_check(target: str) -> Testcase:
    """ Do some basic checks (route, link, ...) """
    _gw, _dev = _gateway(target)
    _gw_reachable: bool = False

    if _dev:
        _dev_flags = _interface_state(_dev)
    else:
        # TODO: dict fromkeys - also in devflags function
        _dev_flags = {'speed': None, 'operstate': None, 'duplex': None}
    if _gw and _gw != "link-local" and _dev_flags['operstate'] == "up":
        _gw_reachable = True if ping(_gw) else False
    # return gateway, interface and interface flags
    # return (_gw, _gw_reachable, _dev, _dev_flags)
    return Testcase(name="base_check",
                    target=target,
                    code=all([_gw, _gw_reachable, _dev, _dev_flags]),
                    blocking=True,
                    output={'gateway': _gw, 'reachable': _gw_reachable, 'dev': _dev, 'flags': _dev_flags})


def _gateway(target: str) -> Tuple[Optional[str], Optional[str]]:
    """ Get gateway to address """
    _gateway: Optional[str]
    _interface: Optional[str]

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

    return (_gateway, _interface)


def _interface_state(interface: str) -> Dict[str, Optional[str]]:
    """ Get interface state """
    _basepath = f"/sys/class/net/{interface}/"

    flags = {'speed': Optional[str],
             'operstate': Optional[str], 'duplex': Optional[str]}

    for flag in flags:
        try:
            with open(f"{_basepath}{flag}") as infile:
                flags[flag] = infile.read().strip()
        except FileNotFoundError:
            print(f"File {_basepath}{flag} not found")

    return flags


@register_plugin
def ping(target: str) -> Optional[Dict[str, str]]:
    """ Run the ping command """
    rtts: Optional[Dict[str, str]]

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
        rtts = None

    return rtts
