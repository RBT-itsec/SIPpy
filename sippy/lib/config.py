# Copyright (c) 2019 ARGE Rundfunk-Betriebstechnik. MIT license, see LICENSE file.

"""
Config class

TODO: add support for plugin configuration
"""
# pylint: disable=W1203

import json
import logging
from typing import Dict, List

from sippy.lib.objects import Target, Testcase

from sippy import plugins


LOGGER = logging.getLogger("SIPpy.Config")


class Config():
    """ Holds all configuration data for SIPpy """

    def __init__(self, filename=None):
        self.filename = filename
        self.setup()
        if self.filename:
            self.from_file(self.filename)

    def setup(self):
        """ Setup/clear all elements """
        self.config = None
        self._blocking_tests: List[str] = []
        self._tests: List[Testcase] = []
        self._targets: List[Target] = []

    @property
    def blocking_tests(self) -> List[str]:
        """ Return a list of all blocking testcases """
        return self._blocking_tests

    @blocking_tests.setter
    def blocking_tests(self, value):
        """ Get all blocking tests from json """
        _tests = value.get('blocking')
        if _tests:
            if not isinstance(_tests, list):
                _tests = list(_tests)
            for _test in _tests:
                self._blocking_tests.append(_test)

    @property
    def targets(self) -> List[Target]:
        """ Return a list of all targets """
        return self._targets

    @targets.setter
    def targets(self, value: Dict):
        """ Get all targets from json file """
        if not value:
            LOGGER.critical(f"No target data in config")
        for target, options in value.items():
            _addr = options.get('addr')
            if not _addr:
                LOGGER.warning(f"No adress found for {target}")
            _tests = options.get('tests')
            if not _tests:
                LOGGER.warning(f"No tests found for {target}")
            if _addr and _tests:
                self._targets.append(Target(name=target, addr=_addr))

    @property
    def tests(self) -> List[Testcase]:
        """ Return a list of all testcases """
        return self._tests

    @tests.setter
    def tests(self, value: Dict):
        """ Get all testcases from json file """
        for target, options in value.items():
            _addr = options.get('addr')
            _tests = options.get('tests')
            if _tests:
                if not isinstance(_tests, list):
                    _tests = list(_tests)
                _unavailable = [t for t in _tests if t not in dir(plugins)]
                _available = [t for t in _tests if t in dir(plugins)]
                if _unavailable:
                    LOGGER.warning(
                        f"Test(s) {_unavailable} for target {target} not found as plugin")
                if _addr and _available:
                    for test in _available:
                        _plugin = getattr(plugins, test)  # get matching plugin
                        if test in self.blocking_tests:
                            self._tests.append(Testcase(name=test, target=Target(
                                name=target, addr=_addr), plugin=_plugin, blocking=True))
                        else:
                            self._tests.append(Testcase(name=test, target=Target(
                                name=target, addr=_addr), plugin=_plugin))
            else:
                LOGGER.warning(f"No tests found for target {target}")

    def from_file(self, filename: str):
        """ Read JSON config from file """
        self.setup()  # reset all configuration items
        try:
            self.config = json.load(open(filename, 'r'))
            self.blocking_tests = self.config.get('plugins')
            self.targets = self.config.get('targets')
            self.tests = self.config.get('targets')
        except FileNotFoundError:
            LOGGER.critical(f"Configuration file {filename} not found!")
        except json.JSONDecodeError:
            LOGGER.critical(f"Could not decode data from {filename}!")
