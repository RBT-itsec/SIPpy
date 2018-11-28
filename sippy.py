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
from lib.clioutput import CLIOutput


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
        plugin = getattr(plugins, testcase.name)
        # print(testcase.name, plugin, plugin.config)
        testcase.category = plugin.category
        testcase.output = plugin.run(testcase.target.addr)
        if testcase.output:
            testcase.returncode = all(testcase.output.values())
        else:
            testcase.returncode = False
        if testcase.blocking and not testcase.returncode:
            LOGGER.critical(
                f"Error running blocking test {testcase.name}. Quitting.")
            return
        # LOGGER.info(
        #    f"{testcase.target.name}: {testcase.name} = {testcase.output}")
        CLIOutput.report(testcase)
    
    # finally report codec tests
    CLIOutput.report_codecs()


if __name__ == "__main__":
    main()
