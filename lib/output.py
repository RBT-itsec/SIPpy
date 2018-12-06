"""
CLI Output of test results
"""

from typing import List, TypeVar

from lib.objects import Testcase
from . import Fore, Back
from plugins.performance import IperfTCPCodec, IperfUDPCodec


# Use Type[T] when using @classmethod/class, else just T for instances
OutputT = TypeVar('OutputT', bound='Output')


class Output():
    """ Generic output """
    @classmethod
    def report_connectivity(cls, testcase: Testcase):
        """ Report connectivity tests """
        pass

    @classmethod
    def report_codecs(cls, testcases: List[Testcase]):
        """ Report codec tests """
        pass


class CLIOutput(Output):
    """ Simple CLI output """
    @classmethod
    def report_connectivity(cls, testcase: Testcase):
        if testcase.returncode:
            print(
                f"{Fore.GREEN}[ISOK]{Fore.RESET} {testcase.target.name} ({testcase.target.addr}) | {testcase.name}: {testcase.output}")
        else:
            print(
                f"{Fore.RED}[FAIL]{Fore.RESET} {testcase.target.name} ({testcase.target.addr}) | {testcase.name}: {testcase.output}")

    @classmethod
    def report_codecs(cls, testcases: List[Testcase]):
        # Sort Codecs by TCP and UDP
        udpcodecs = [
            testcase for testcase in testcases if isinstance(testcase.plugin, IperfUDPCodec)]
        tcpcodecs = [
            testcase for testcase in testcases if isinstance(testcase.plugin, IperfTCPCodec)]

        if udpcodecs:
            cls.report_udp(udpcodecs)
        if tcpcodecs:
            cls.report_tcp(tcpcodecs)

    @classmethod
    def report_udp(cls, testcases: List[Testcase]):
        """ Report UDP Testcases """
        header = {"jitter_ms": "Jitter (ms)", "lost_packets": "Packets lost",
                  "lost_percent": "Lost %", "mbps": "MBps"}

        header_str = "{:^15} | {jitter_ms:^15} | {lost_packets:^15} | {lost_percent:^15} | {mbps:^15}".format(
            "UDP Codec", **header)
        output_str = "{:^15} | {jitter_ms:^15.5} | {lost_packets:^15} | {lost_percent:^15} | {mbps:^15.5}"

        CLIOutput._report(testcases, header_str, output_str)

    @classmethod
    def report_tcp(cls, testcases: List[Testcase]):
        """ Report TCP Testcases """
        header = {"retransmits": "Retransmits",
                  "sent_mbps": "MBps sent", "rcvd_mbps": "MBps received"}

        header_str = "{:^15} | {retransmits:^15} | {sent_mbps:^15} | {rcvd_mbps:^15}".format(
            "TCP Codec", **header)
        output_str = "{:^15} | {retransmits:^15} | {sent_mbps:^15.5} | {rcvd_mbps:^15.5}"

        CLIOutput._report(testcases, header_str, output_str)

    @classmethod
    def _report(cls, testcases: List[Testcase], header: str, output_fmt: str):
        """ Function to report codec information based on header and output formats """
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        for testcase in testcases:
            name = testcase.name
            if testcase.returncode:
                name = f"{Fore.GREEN}{name}{Fore.RESET}"
                print(output_fmt.format(name, **testcase.output))
            else:
                name = f"{Fore.RED}{name}{Fore.RESET}"
                print("{:^14} | ERROR".format(name))
        print("-" * len(header))
