"""
Created on 10 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdVCalBaseline(object):
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
        self.__parser = optparse.OptionParser(usage="%prog [{ -b GAS  | -s GAS VALUE | -m GAS MINIMUM | -r GAS | -d }] "
                                                    "[-v]", version="%prog 1.0")

        # functions...
        self.__parser.add_option("--baseline", "-b", type="string", nargs=1, action="store", dest="baseline",
                                 help="report offset for GAS")

        self.__parser.add_option("--set", "-s", type="string", nargs=2, action="store", dest="set",
                                 help="set offset for GAS to integer VALUE")

        self.__parser.add_option("--match", "-m", type="string", nargs=2, action="store", dest="match",
                                 help="set offset for GAS to match MINIMUM of the compendium")

        self.__parser.add_option("--remove", "-r", type="string", nargs=1, action="store", dest="remove",
                                 help="remove the baseline for the given GAS")

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

        if self.match is not None:
            param_count += 1

        if self.remove is not None:
            param_count += 1

        if self.delete:
            param_count += 1

        if param_count > 1:
            return False

        # validate VALUE...
        if self.set is not None and not self.__is_integer(self.set[1]):
            return False

        if self.match is not None and not self.__is_integer(self.match[1]):
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def gas_name(self):
        if self.baseline:
            return self.baseline

        if self.set:
            return self.set[0]

        if self.match:
            return self.match[0]

        if self.remove:
            return self.remove[0]

        return None


    def update(self):
        return self.set is not None or self.match is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def baseline(self):
        return self.__opts.baseline


    @property
    def set(self):
        return self.__opts.set


    def set_value(self):
        return None if self.set is None else int(self.set[1])


    @property
    def match(self):
        return self.__opts.match


    def match_value(self):
        return None if self.match is None else int(self.match[1])


    @property
    def remove(self):
        return self.__opts.remove


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
        return "CmdVCalBaseline:{baseline:%s, set:%s, match:%s, remove:%s, delete:%s, verbose:%s}" % \
               (self.baseline, self.set, self.match, self.remove, self.delete, self.verbose)
