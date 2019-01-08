# Copyright (c) 2019 ARGE Rundfunk-Betriebstechnik. MIT license, see LICENSE file.

"""
Common objects
"""

from dataclasses import dataclass, field
from typing import Dict

from plugins import Plugin


@dataclass
class Target():
    """ Represents a test target """
    name: str
    addr: str


@dataclass
class PluginConfig():
    """ Represents a plugins configuration """
    name: str
    options: Dict


@dataclass
class Testcase():
    """ Represents a testcase """
    name: str  # Name of the plugin to run
    target: Target
    plugin: Plugin
    # category: str = "generic"  # Name of the plugins category
    # config: PluginConfig  # Testcase specific config or default config
    returncode: bool = False
    blocking: bool = False
    output: Dict = field(default_factory=dict)
    # config: Dict = field(default_factory=dict)
