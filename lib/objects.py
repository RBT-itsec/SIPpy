"""
Common objects
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Testcase():
    name: str
    target: str
    # finished: bool
    code: bool
    blocking: bool
    output: Dict
