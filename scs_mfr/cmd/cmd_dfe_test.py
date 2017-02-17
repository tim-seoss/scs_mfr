"""
Created on 2 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdDFETest(object):
    """unix command line handler"""

    def __init__(self):
        """stuff"""
        self.__parser = optparse.OptionParser(usage="%prog SERIAL_NUMBER [-g] [-n] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--gps", "-g", action="store_true", dest="ignore_gps", default=False,
                                 help="ignore GPS module")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.serial_number is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def serial_number(self):
        return self.__args[0] if len(self.__args) > 0 else None


    @property
    def ignore_gps(self):
        return self.__opts.ignore_gps


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
        return "CmdDFETest:{serial_number:%s, ignore_gps:%s, verbose:%s, args:%s}" % \
                    (self.serial_number, self.ignore_gps, self.verbose, self.args)
