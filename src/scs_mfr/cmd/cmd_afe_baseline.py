"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdAFEBaseline(object):
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
        self.__parser = optparse.OptionParser(usage="%prog { { -s | -u | -d } GAS VALUE | -z } [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--set", "-s", type="string", nargs=2, action="store", dest="set",
                                 help="set offset for GAS to integer VALUE")

        self.__parser.add_option("--up", "-u", type="string", nargs=2, action="store", dest="up",
                                 help="move offset up for GAS, by integer VALUE")

        self.__parser.add_option("--down", "-d", type="string", nargs=2, action="store", dest="down",
                                 help="move offset down for GAS, by integer VALUE")

        self.__parser.add_option("--zero", "-z", action="store_true", dest="zero",
                                 help="zero all baseline offsets")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        param_count = 0

        if self.set is not None:
            param_count += 1

        if self.up is not None:
            param_count += 1

        if self.down is not None:
            param_count += 1

        if self.zero is not None:
            param_count += 1

        if param_count > 1:
            return False

        if self.set is not None and not self.__is_integer(self.set[1]):
            return False

        if self.up is not None and not self.__is_integer(self.up[1]):
            return False

        if self.down is not None and not self.__is_integer(self.down[1]):
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def gas_name(self):
        if self.set:
            return self.set[0]

        if self.up:
            return self.up[0]

        if self.down:
            return self.down[0]

        return None


    def offset_value(self):
        if self.set:
            return int(self.set[1])

        if self.up:
            return int(self.up[1])

        if self.down:
            return int(self.down[1])

        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def set(self):
        return self.__opts.set


    @property
    def up(self):
        return self.__opts.up


    @property
    def down(self):
        return self.__opts.down


    @property
    def zero(self):
        return self.__opts.zero


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdAFEBaseline:{set:%s, up:%s, down:%s, zero:%s, verbose:%s, args:%s}" % \
               (self.set, self.up, self.down, self.zero, self.verbose, self.args)
