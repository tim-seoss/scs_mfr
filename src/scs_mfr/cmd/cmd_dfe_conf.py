"""
Created on 27 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdDFEConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __addr_str(cls, addr):
        if addr is None:
            return None

        return "0x%02x" % addr


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{ -s [-p ADDR] | -d }] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--set", "-s", action="store_true", dest="set", default=False,
                                 help="create or update a DFE configuration")

        self.__parser.add_option("--pt1000", "-p", type="int", nargs=1, action="store", dest="pt1000",
                                 help="set I2C address of the Pt1000 ADC (if present)")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the DFE configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if not self.set() and self.pt1000_addr is not None:
            return False

        return True


    def set(self):
        return self.__opts.set


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pt1000_addr(self):
        return self.__opts.pt1000


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
        return "CmdDFEConf:{set:%s, pt1000:%s, delete:%s, verbose:%s}" % \
               (self.set(), CmdDFEConf.__addr_str(self.pt1000_addr), self.delete, self.verbose)
