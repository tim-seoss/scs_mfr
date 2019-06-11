"""
Created on 27 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_dfe.board.dfe_conf import DFEConf


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
        self.__parser = optparse.OptionParser(usage="%prog [{ -s SOURCE [-p ADDR] | -d }] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--source", "-s", type="string", nargs=1, action="store", dest="source",
                                 help="sensor equipment (AFE or IEI)")

        self.__parser.add_option("--pt1000", "-p", type="int", nargs=1, action="store", dest="pt1000",
                                 help="set I2C address of the Pt1000 ADC (if present, AFE only)")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the DFE configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.set() and self.source not in DFEConf.sources():
            return False

        if self.source != 'AFE' and self.pt1000_addr is not None:
            return False

        if not self.set() and self.pt1000_addr is not None:
            return False

        return True


    def set(self):
        return self.__opts.source is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def source(self):
        return self.__opts.source


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
        return "CmdDFEConf:{source:%s, pt1000:%s, delete:%s, verbose:%s}" % \
               (self.source, CmdDFEConf.__addr_str(self.pt1000_addr), self.delete, self.verbose)
