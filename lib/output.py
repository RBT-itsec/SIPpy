"""
CLI Output of test results
"""

from typing import List, TypeVar

from lib.objects import Testcase


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
            testcase for testcase in testcases if "jitter_ms" in testcase.output]
        tcpcodecs = [
            testcase for testcase in testcases if "retransmits" in testcase.output]

        if udpcodecs:
            cls.report_udp(udpcodecs)
        if tcpcodecs:
            cls.report_tcp(tcpcodecs)

    @classmethod
    def report_udp(cls, testcases: List[Testcase]):
        """ Report UDP Testcases """
        header = {"jitter_ms": "Jitter (ms)", "lost_packets": "Packets lost",
                  "lost_percent": "Lost %", "mbps": "MBps"}

        # TODO: make cleaner - f-strings possible?
        header_str = f"{'Codec':^10} | \
                        {header['jitter_ms']:^10} | \
                        {header['lost_packets']:^10} | \
                        {header['lost_percent']:^10} | \
                        {header['mbps']:^10}"

        print(header_str)
        print("-" * len(header_str))

        for testcase in testcases:
            if testcase.returncode:
                _output = testcase.output
                print("{:^10} | {jitter_ms:^10.8} | {lost_packets:^10} | {lost_percent:^10.8} | {mbps:^10.8}".format(
                    testcase.name, **_output))
            else:
                # TODO: specify error
                print("{:^10} | ERROR".format(testcase.name))

    @classmethod
    def report_tcp(cls, testcases: List[Testcase]):
        """ Report TCP Testcases """
        header = {"retransmits": "Retransmits",
                  "sent_mbps": "MBps sent", "rcvd_mbps": "MBps received"}

        header_str = f"{'Codec':^10} | \
                        {header['retransmits']:^10} | \
                        {header['sent_mbps']:^10} | \
                        {header['rcvd_mbps']:^10}"

        print(header_str)
        print("-" * len(header_str))

        for testcase in testcases:
            if testcase.returncode:
                _output = testcase.output
                print("{:^10} | {retransmits:^10.8} | {sent_mbps:^10.8} | {rcvd_mbps:^10.8}".format(
                    testcase.name, **_output))
            else:
                # TODO: specify error
                print("{:^10} | ERROR".format(testcase.name))

        # if testcase.returncode:
        #     print(
        #         f"[ISOK] {testcase.target.name} ({testcase.target.addr}) | {testcase.name}: {testcase.output}")
        # else:
        #     print(
        #         f"[FAIL] {testcase.target.name} ({testcase.target.addr}) | {testcase.name}: {testcase.output}")
