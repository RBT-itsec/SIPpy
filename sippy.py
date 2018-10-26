"""

(c) jakob.pfister@rbt-nbg.de
"""
# pylint: disable=W1203


import logging
from secrets import randbits


import plugins
from lib.config import Config


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(name="SIPpy")


def main() -> None:
    """ The main foo """
    LOGGER.info(f"Starting up...")
    LOGGER.info(f"Checking weather forecast.")
    LOGGER.info(f"Lucky bits for today are: {randbits(42)}")

    config = Config("config.json")

    for testcase in config.tests:
        func = getattr(plugins, testcase.name)
        testcase.output = func(testcase.target.addr)
        testcase.returncode = all(testcase.output.values())
        if testcase.blocking and not testcase.returncode:
            print(f"Error running blocking test {testcase.name}. Quitting.")
            return
        print(testcase)


if __name__ == "__main__":
    main()
