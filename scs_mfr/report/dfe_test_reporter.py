"""
Created on 29 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys


# --------------------------------------------------------------------------------------------------------------------

class TestReporter(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__passed = True


    # ----------------------------------------------------------------------------------------------------------------

    def report_test(self, result):
        report = 'OK' if result else 'FAIL'

        print(report, file=sys.stderr)
        print("-", file=sys.stderr)

        if not result:
            self.__passed = False


    def report_exception(self, exception, is_fatal):
        print(exception.__class__.__name__, file=sys.stderr)

        self.__passed = False

        if is_fatal:
            print("-", file=sys.stderr)
            raise exception


    def report_result(self):
        report = 'OK' if self.__passed else 'FAIL'

        print("result: %s" % report, file=sys.stderr)
        print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def passed(self):
        return self.__passed


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TestReporter:{passed:%s}" % (self.passed)
