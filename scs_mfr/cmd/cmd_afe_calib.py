"""
Created on 27 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdAFECalib(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{-s AFE_SERIAL_NUMBER | -t}] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--set", "-s", type="string", nargs=1, action="store", dest="serial_number",
                                 help="set AFE serial number")

        self.__parser.add_option("--test", "-t", action="store_true", dest="test", default=False,
                                 help="set AFE to test load")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.serial_number is not None & self.test:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.serial_number is not None or self.test


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def serial_number(self):
        return self.__opts.serial_number


    @property
    def test(self):
        return self.__opts.test


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
        return "CmdAFECalib:{serial_number:%s, test:%s, verbose:%s, args:%s}" % \
               (self.serial_number, self.test, self.verbose, self.args)
