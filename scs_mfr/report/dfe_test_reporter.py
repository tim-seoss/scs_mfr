"""
Created on 29 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from collections import OrderedDict


# --------------------------------------------------------------------------------------------------------------------

class DFETestReporter(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__passed = True
        self.__subjects = OrderedDict()


    # ----------------------------------------------------------------------------------------------------------------

    def report_test(self, subject, ok):
        report = 'OK' if ok else 'FAIL'

        self.__subjects[subject] = report

        print(report, file=sys.stderr)
        print("-", file=sys.stderr)

        if not ok:
            self.__passed = False


    def report_exception(self, subject, exception):
        report = exception.__class__.__name__

        self.__subjects[subject] = report

        print(report, file=sys.stderr)
        print("-", file=sys.stderr)

        self.__passed = False


    def report_result(self):
        report = 'OK' if self.__passed else 'FAIL'

        print("result: %s" % report, file=sys.stderr)
        print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def passed(self):
        return self.__passed


    @property
    def subjects(self):
        return self.__subjects


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DFETestReporter:{passed:%s, subjects:%s}" % (self.passed, self.subjects)
