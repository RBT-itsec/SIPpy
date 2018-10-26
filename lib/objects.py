"""
Common objects
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Target():
    name: str
    addr: str


@dataclass
class Testcase():
    name: str
    target: Target
    returncode: bool = False
    blocking: bool = False
    output: Dict = field(default_factory=dict)


@dataclass
class PluginConfig():
    name: str
    options: Dict
