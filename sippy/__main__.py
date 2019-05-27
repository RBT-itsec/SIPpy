# Copyright (c) 2019 ARGE Rundfunk-Betriebstechnik. MIT license, see LICENSE file.

"""

(c) jakob.pfister@rbt-nbg.de
TODO: Add argparse -> TUI or GUI
TODO: Add ability to change local ethernet address (test-interface)
TODO: Add CLI frontend
TODO: optional add GUI frontend
"""
# pylint: disable=W1203


import logging
import os
from secrets import randbits

from sippy import BASE_PATH
from sippy import plugins
from sippy.lib.config import Config
from sippy.lib.output import CLIOutput
from sippy.lib.reporthandler import ReportHandler


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(name="SIPpy")


def main() -> None:
    """ The main foo """
    LOGGER.info(f"Starting up...")
    LOGGER.info(f"Checking weather forecast.")
    LOGGER.info(f"Lucky bits for today are: {randbits(42)}")

    LOGGER.info(f"The following plugins are available: {dir(plugins)}")

    LOGGER.info(f"Loading configuration")
    config = Config(os.path.join(BASE_PATH, "config.json"))

    for testcase in config.tests:
        LOGGER.info(
            f"Running test {testcase.name} against {testcase.target.name}")
            # TODO: Let reporter print Testcase x/num
        testcase.output = testcase.plugin.run(testcase.target.addr)
        if testcase.output:
            # testcase.returncode = True if testcase.output.values() else False
            testcase.returncode = all(True if x is not None else False for x in testcase.output.values())
            # testcase.returncode = all(testcase.output.values())  # fails with codec tests
            # when e.g. paket loss = 0
        else:
            testcase.returncode = False
        if testcase.blocking and not testcase.returncode:
            LOGGER.critical(
                f"Error running blocking test {testcase.name}. Quitting.")
            return
        # add testcast to ReportHandler and report from there to <X>-Output
        ReportHandler.add_report(testcase, CLIOutput)
    ReportHandler.report(CLIOutput)  # control output via args



if __name__ == "__main__":
    main()
