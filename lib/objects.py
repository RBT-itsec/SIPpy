"""
Common objects
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Target():
    """ Represents a test target """
    name: str
    addr: str


@dataclass
class Testcase():
    """ Represents a testcase """
    name: str
    target: Target
    returncode: bool = False
    blocking: bool = False
    output: Dict = field(default_factory=dict)


@dataclass
class PluginConfig():
    """ Represents a plugins configuration """
    name: str
    options: Dict
