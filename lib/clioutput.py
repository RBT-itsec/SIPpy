"""
CLI Output of test results
"""

from lib.objects import Testcase
from typing import Dict


class CLIOutput():
    """ Simple CLI output """
    codecreports: Dict = {}

    # def __init__(self):
    # self.codecreports = {}

    @classmethod
    def report(cls, testcase: Testcase):
        """ Report the results of a testcase """
        if testcase.plugin.category == "codec":  # if testcase is codec, store it
            cls.codecreports[testcase.name] = testcase.output
        else:  # if no codec
            print(testcase.output)

    @classmethod
    def report_codecs(cls):
        for codec, result in cls.codecreports.items():
            print(f"Codec: {codec}")
            print(f"{result}")
            print(f"---")
            # make a table depending on tcp/udp - pass codec protocol
