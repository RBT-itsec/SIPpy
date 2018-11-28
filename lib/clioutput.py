""" 
CLI Output of test results
"""

from lib.objects import Testcase

class CLIOutput():
    def __init__(self):
        pass

    @classmethod
    def report(cls, testcase: Testcase):
        """ Report the results of a testcase """
        print(testcase.output)