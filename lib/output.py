"""
CLI Output of test results
"""

from typing import TypeVar

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
    def report_codec(cls, testcase: Testcase):
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
    def report_codec(cls, testcase: Testcase):
        # make table !
        if testcase.returncode:
            print(
                f"[ISOK] {testcase.target.name} ({testcase.target.addr}) | {testcase.name}: {testcase.output}")
        else:
            print(
                f"[FAIL] {testcase.target.name} ({testcase.target.addr}) | {testcase.name}: {testcase.output}")
