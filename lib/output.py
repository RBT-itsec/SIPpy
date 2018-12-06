"""
CLI Output of test results
"""

from typing import List, TypeVar

from lib.objects import Testcase
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
                f"[ISOK] {testcase.target.name} ({testcase.target.addr}) | {testcase.name}: {testcase.output}")
        else:
            print(
                f"[FAIL] {testcase.target.name} ({testcase.target.addr}) | {testcase.name}: {testcase.output}")

    @classmethod
    def report_codecs(cls, testcases: List[Testcase]):
        # make table !
        # Sort Codecs by TCP and UDP
        # TODO: Check with ifisinstace
        udpcodecs = [
            testcase for testcase in testcases if isinstance(testcase, IperfUDPCodec)]
            # testcase for testcase in testcases if "jitter_ms" in testcase.output]
        tcpcodecs = [
            testcase for testcase in testcases if isinstance(testcase, IperfTCPCodec)]
            # testcase for testcase in testcases if "retransmits" in testcase.output]

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
            if testcase.returncode:
                print(output_fmt.format(testcase.name, **testcase.output))
            else:
                print("{:^14} | ERROR".format(testcase.name))
        print("-" * len(header))
