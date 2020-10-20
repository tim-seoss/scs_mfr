"""
Created on 17 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdOPCVersion(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -w | -s } [-n NAME] [-v]", version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--firmware", "-w", action="store_true", dest="firmware", default=False,
                                 help="report firmware version")

        self.__parser.add_option("--serial", "-s", action="store_true", dest="serial", default=False,
                                 help="report serial number")

        # optional...
        self.__parser.add_option("--name", "-n", type="string", nargs=1, action="store", dest="name",
                                 help="the name of the OPC configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if bool(self.firmware) == bool(self.serial):
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def firmware(self):
        return self.__opts.firmware


    @property
    def serial(self):
        return self.__opts.serial


    @property
    def name(self):
        return self.__opts.name


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdOPCVersion:{firmware:%s, serial:%s, name:%s, verbose:%s}" % \
               (self.firmware, self.serial, self.name, self.verbose)
