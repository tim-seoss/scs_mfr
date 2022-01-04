"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdBaseline(object):
    """unix command line handler"""


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __is_integer(value):
        try:
            int(value)
        except ValueError:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ -b GAS  | { -s | -o } GAS VALUE | "
                                                    "-c GAS CORRECT REPORTED | -z | -d }] [-v]", version="%prog 1.0")

        # functions...
        self.__parser.add_option("--baseline", "-b", type="string", nargs=1, action="store", dest="baseline",
                                 help="report offset for GAS")

        self.__parser.add_option("--set", "-s", type="string", nargs=2, action="store", dest="set",
                                 help="set offset for GAS to integer VALUE")

        self.__parser.add_option("--offset", "-o", type="string", nargs=2, action="store", dest="offset",
                                 help="change offset for GAS, by integer VALUE")

        self.__parser.add_option("--correct", "-c", type="string", nargs=3, action="store", dest="correct",
                                 help="change offset for GAS, by the difference between CORRECT and REPORTED values")

        self.__parser.add_option("--zero", "-z", action="store_true", dest="zero", default=False,
                                 help="zero all offsets")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the baseline configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        param_count = 0

        # setters...
        if self.baseline is not None:
            param_count += 1

        if self.set is not None:
            param_count += 1

        if self.offset is not None:
            param_count += 1

        if self.correct is not None:
            param_count += 1

        if self.zero:
            param_count += 1

        if self.delete:
            param_count += 1

        if param_count > 1:
            return False

        # validate VALUE...
        if self.set is not None and not self.__is_integer(self.set[1]):
            return False

        if self.offset is not None and not self.__is_integer(self.offset[1]):
            return False

        if self.correct is not None and \
                (not self.__is_integer(self.correct[1]) or not self.__is_integer(self.correct[2])):
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def gas_name(self):
        if self.baseline:
            return self.baseline

        if self.set:
            return self.set[0]

        if self.offset:
            return self.offset[0]

        if self.correct:
            return self.correct[0]

        return None


    def update(self):
        return self.set or self.offset or self.correct


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def baseline(self):
        return self.__opts.baseline


    @property
    def set(self):
        return self.__opts.set


    def set_value(self):
        return int(self.set[1]) if self.set else None


    @property
    def offset(self):
        return self.__opts.offset


    def offset_value(self):
        return int(self.offset[1]) if self.offset else None


    @property
    def correct(self):
        return self.__opts.correct


    def correct_value(self):
        return int(self.correct[1]) if self.correct else None


    def reported_value(self):
        return int(self.correct[2]) if self.correct else None


    @property
    def zero(self):
        return self.__opts.zero


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdBaseline:{baseline:%s, set:%s, offset:%s, correct:%s, zero:%s, delete:%s, verbose:%s}" % \
               (self.baseline, self.set, self.offset, self.correct, self.zero, self.delete, self.verbose)
