"""

(c) jakob.pfister@rbt-nbg.de
"""

import json
from typing import Dict

import plugins


def load_config(filename: str = './config.json') -> Dict:
    """ Load config from JSON file """
    return json.load(open(filename, 'r'))


def main() -> None:
    """ The main foo """
    # print(f"Parsing config: {load_config()}")
    print(f"Parsing config")
    config = load_config()
    print(config)

    targets = config.get('targets')
    addr_sbc = targets.get('sbc')
    addr_codec = targets.get('codec')
    print(f"SBC: {addr_sbc}, Codec: {addr_codec}")
    # addr_sbc = config.get('targets').get('sbc')
    # addr_codec = config.get('targets').get('codec')
    
    for module, tests in config.get('modules').items():
        print(module, tests)
        for test in tests:
            if test in dir(plugins):
                func = getattr(plugins, test)
                print(func, func.__name__)

    
    # print(f"Route Base Check: {plugins.base_check('172.31.10.13')}")
    # print(f"Local Base Check: {plugins.base_check('192.168.23.10')}")
    # print(f"Ping: {plugins.ping('172.31.10.13')}")  # deprecated


if __name__ == "__main__":
    main()
