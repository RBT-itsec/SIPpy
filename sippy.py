"""

(c) jakob.pfister@rbt-nbg.de
TODO: Add argparse
TODO: Add CLI frontend
TODO: optional add GUI frontend
"""
# pylint: disable=W1203


import logging
from secrets import randbits


import plugins
from lib.config import Config
from lib.output import CLIOutput
from lib.reporthandler import ReportHandler


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(name="SIPpy")


def main() -> None:
    """ The main foo """
    LOGGER.info(f"Starting up...")
    LOGGER.info(f"Checking weather forecast.")
    LOGGER.info(f"Lucky bits for today are: {randbits(42)}")

    LOGGER.info(f"The following plugins are available: {dir(plugins)}")

    LOGGER.info(f"Loading configuration")
    config = Config("config.json")

    for testcase in config.tests:
        LOGGER.info(
            f"Running test {testcase.name} against {testcase.target.name}")
        testcase.output = testcase.plugin.run(testcase.target.addr)
        if testcase.output:
            testcase.returncode = all(testcase.output.values())
        else:
            testcase.returncode = False
        if testcase.blocking and not testcase.returncode:
            LOGGER.critical(
                f"Error running blocking test {testcase.name}. Quitting.")
            return
        # add testcast to ReportHandler and report from there to <X>-Output
        ReportHandler.add_report(testcase)
    ReportHandler.report(CLIOutput)  # control output via args



if __name__ == "__main__":
    main()
