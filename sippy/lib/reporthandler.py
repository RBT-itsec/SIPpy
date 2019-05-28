# Copyright (c) 2019 ARGE Rundfunk-Betriebstechnik. MIT license, see LICENSE file.

"""
Handle reporting of testcases
"""

from typing import List
from typing import Type, Optional

from .objects import Testcase
from .output import OutputT


class ReportHandler():
    """ Handle reporting of Testcases """
    connectivity_reports: List = []
    codec_reports: List = []
    reported: List = []

    @classmethod
    def reset(cls) -> None:
        """ Reset all reports """
        cls.connectivity_reports = []
        cls.codec_reports = []
        cls.reported = []

    @classmethod
    def add_report(cls, testcase: Testcase, output: Optional[Type[OutputT]] = None) -> None:
        """ Add a testcase to the reports, report immediately if output is given and testcase
        if in a matching category """
        if testcase.plugin.category == "connectivity":
            if output:  # if output is given, report connectivity test immidiately
                output.report_connectivity(testcase)
                cls.reported.append(testcase)
            else:
                cls.connectivity_reports.append(testcase)
        if testcase.plugin.category == "codec":
            # make tcp and udp reports?
            cls.codec_reports.append(testcase)

    @classmethod
    def report(cls, output: Type[OutputT]) -> None:
        """ Report all the testcases """
        for report in cls.connectivity_reports:
            if report not in cls.reported:  # only report if not reported immediately
                output.report_connectivity(report)
        # for report in cls.codec_reports:
        output.report_codecs(cls.codec_reports)

    @classmethod
    def get_connectivity_reports(cls) -> List[Testcase]:
        return cls.connectivity_reports

    @classmethod
    def get_codec_reports(cls) -> List[Testcase]:
        return cls.codec_reports
