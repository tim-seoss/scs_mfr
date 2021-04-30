"""
Created on 30 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdModem(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -c | -s } [-v]", version="%prog 1.0")

        # modem...
        self.__parser.add_option("--connection", "-c", action="store_true", dest="connection", default=False,
                                 help="report on modem connection ")

        self.__parser.add_option("--sim", "-s", action="store_true", dest="sim", default=False,
                                 help="report on SIM")

        # narrative...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.connection == self.sim:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def connection(self):
        return self.__opts.connection


    @property
    def sim(self):
        return self.__opts.sim


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdModem:{connection:%s, sim:%s, verbose:%s}" % (self.connection, self.sim, self.verbose)
