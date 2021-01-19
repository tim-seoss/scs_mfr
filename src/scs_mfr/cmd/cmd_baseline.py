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
        self.__parser = optparse.OptionParser(usage="%prog [{ { { -s | -o } GAS VALUE | -c GAS CORRECT REPORTED } "
                                                    "[-r HUMID -t TEMP [-p PRESS]] | -z }] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--set", "-s", type="string", nargs=2, action="store", dest="set",
                                 help="set offset for GAS to integer VALUE")

        self.__parser.add_option("--offset", "-o", type="string", nargs=2, action="store", dest="offset",
                                 help="change offset for GAS, by integer VALUE")

        self.__parser.add_option("--correct", "-c", type="string", nargs=3, action="store", dest="correct",
                                 help="change offset for GAS, by the difference between CORRECT and REPORTED values")

        self.__parser.add_option("--humid", "-r", type="float", nargs=1, action="store", dest="humid",
                                 help="record relative humidity value (%)")

        self.__parser.add_option("--temp", "-t", type="float", nargs=1, action="store", dest="temp",
                                 help="record temperature value (°C)")

        self.__parser.add_option("--press", "-p", type="float", nargs=1, action="store", dest="press",
                                 help="record barometric pressure value (kPa)")

        self.__parser.add_option("--zero", "-z", action="store_true", dest="zero",
                                 help="zero all offsets")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        param_count = 0

        # setters...
        if self.set is not None:
            param_count += 1

        if self.offset is not None:
            param_count += 1

        if self.correct is not None:
            param_count += 1

        if self.zero is not None:
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

        # environment...
        if bool(self.humid is None) != bool(self.temp is None):
            return False

        return True


    def env_is_specified(self):
        return self.humid is not None and self.temp is not None


    # ----------------------------------------------------------------------------------------------------------------

    def gas_name(self):
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
    def humid(self):
        return self.__opts.humid


    @property
    def temp(self):
        return self.__opts.temp


    @property
    def press(self):
        return self.__opts.press


    @property
    def zero(self):
        return self.__opts.zero


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdBaseline:{set:%s, offset:%s, correct:%s, humid:%s, temp:%s, press:%s, zero:%s, verbose:%s}" % \
               (self.set, self.offset, self.correct, self.humid, self.temp, self.press, self.zero, self.verbose)
