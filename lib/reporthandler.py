"""
Handle reporting of testcases
"""

from typing import List

from typing import Type
from .objects import Testcase
from .output import OutputT



class ReportHandler():
    """ Handle reporting of Testcases """
    connectivity_reports: List = []
    codec_reports: List = []

    @classmethod
    def reset(cls):
        """ Reset all reports """
        cls.reports = []

    @classmethod
    def add_report(cls, testcase: Testcase):
        """ Add a testcase to the reports """
        if testcase.plugin.category == "connectivity":
            cls.connectivity_reports.append(testcase)
        if testcase.plugin.category == "codec":
            # make tcp and udp reports?
            cls.codec_reports.append(testcase)

    @classmethod
    def report(cls, output: Type[OutputT]):
        """ Report all the testcases """
        for report in cls.connectivity_reports:
            output.report_connectivity(report)
        for report in cls.codec_reports:
            output.report_codec(report)
