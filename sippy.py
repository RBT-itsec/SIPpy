"""

(c) jakob.pfister@rbt-nbg.de
"""

import json
import logging
from secrets import randbits
from typing import Dict

import plugins
from lib.config import Config


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(name="SIPpy")


def main() -> None:
    """ The main foo """
    LOGGER.info(f"Starting up...")
    LOGGER.info(f"Checking weather forecast.")
    LOGGER.info(f"Lucky bits for today are: {randbits(42)}")

    config = Config()
    config.from_file("config.json")
    print(config.targets)
    print(config.tests)

    for target, addr in config.targets.items():
        tests = config.tests.get(target)
        # print(f"Target {target} has tests: {tests}")
        if tests:
            for test in tests:
                func = getattr(plugins, test)
                result = func(addr)  # run the plugin with a given target
                print(f"{test} on {addr}: {result}")


if __name__ == "__main__":
    main()
