"""
Config class

TODO: add support for plugin configuration
"""
# pylint: disable=W1203

import json
import logging
from typing import Dict

import plugins


LOGGER = logging.getLogger("SIPpy.Config")


class Config():
    """ Represents the config for the tests """

    def __init__(self, filename=None):
        self.config = None
        self._targets = {}
        self.plugins = []
        self._tests = {}
        if filename:
            self.from_file(filename)

    @property
    def targets(self) -> Dict:
        """ Return all the targets in the config """
        return self._targets

    @targets.setter
    # add types for second dict [str, List] ? accept also [str, str]
    def targets(self, value: Dict[str, Dict]):
        """ Set the targets and tests cases. """
        # TODO: Move tests into separate property
        if not value:
            LOGGER.critical(f"No target data in config")
        for target, options in value.items():
            _addr = options.get('addr')
            if not _addr:
                LOGGER.warning(f"No address found for {target}")

            _tests = options.get('tests')
            if _tests:
                if not isinstance(_tests, list):
                    _tests = list(_tests)
                _failed = [test for test in _tests if test not in dir(plugins)]
                _tests = [test for test in _tests if test in dir(plugins)]
                if _failed:
                    LOGGER.warning(f"Test(s) {_failed} not found as Plugin for target {target}.")
                if _tests and _addr:
                    self._targets[target] = _addr
                    self._tests[target] = _tests
            else:
                LOGGER.warning(
                    f"No tests found for target {target}. Removing from test config.")

    @property
    def tests(self) -> Dict:
        """ Return all tests in the configuration """
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
