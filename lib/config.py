"""
Config class

TODO: add support for plugin configuration
"""

import json
import logging
import plugins
from typing import Dict


LOGGER = logging.getLogger("SIPpy.Config")


class Config():
    def __init__(self):
        self.config = None
        self._targets = {}
        self.plugins = []
        self._tests = {}

    @property
    def targets(self) -> Dict:
        return self._targets

    @targets.setter
    def targets(self, value: Dict[str, Dict]):  # add types for second dict [str, List] ? accept also [str, str]
        if not value:
            LOGGER.critical(f"No target data in config")
        for target, options in value.items():
            _addr = options.get('addr')
            if not _addr:
                LOGGER.critical(f"No address found for {target}")

            _tests = options.get('tests')
            if _tests:
                if not isinstance(_tests, list):
                    _tests = list(_tests)
                _failed = [test for test in _tests if test not in dir(plugins)]
                _tests = [test for test in _tests if test in dir(plugins)]
                if _failed:
                    LOGGER.warning(f"Test(s) {_failed} not found as Plugin.")
                if _tests and _addr:
                    self._targets[target] = _addr
                    self._tests[target] = _tests
            else:
                LOGGER.critical(f"No tests found for target {target}. Removing from test config.")

    @property
    def tests(self) -> Dict:
        return self._tests

    def from_file(self, filename: str):
        """ Read JSON config from file """
        self.__init__()  # reset all configuration items
        try:
            self.config = json.load(open(filename, 'r'))
            self.targets = self.config.get('targets')
        except FileNotFoundError:
            LOGGER.critical(f"Configuration file {filename} not found!")
        except json.JSONDecodeError:
            LOGGER.critical(f"Could not decode data from {filename}!")

    # def _check_config(self):
    #     """ Check config for completeness and errors """
    #     # Get all used plugins from config and check if they are available
        
        
