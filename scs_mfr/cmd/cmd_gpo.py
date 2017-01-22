"""
Created on 24 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdGPO(object):
    """
    unix command line handler
    """

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog PIN LEVEL [-w PERIOD] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--wait", "-w", type="int", nargs=1, action="store", default=0, dest="wait", help="wait period (default for-ever = 0)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False, help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.pin is None or self.level is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pin(self):
        return self.__args[0].upper() if len(self.__args) > 0 else None


    @property
    def level(self):
        return int(self.__args[1]) if len(self.__args) > 1 else None


    @property
    def wait(self):
        return self.__opts.wait


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
        return "CmdGPO:{pin:%s, level:%s, wait:%s, verbose:%s, args:%s}" % \
                    (self.pin, self.level, self.wait, self.verbose, self.args)
