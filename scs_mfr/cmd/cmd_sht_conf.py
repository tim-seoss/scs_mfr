"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdSHTConf(object):
    """unix command line handler"""

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [-i INT_ADDR] [-e EXT_ADDR] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--int-addr", "-i", type="int", nargs=1, action="store", dest="int_addr", default=None,
                                 help="I2C address of SHT in A4 package")

        self.__parser.add_option("--ext-addr", "-e", type="int", nargs=1, action="store", dest="ext_addr", default=None,
                                 help="I2C address of SHT exposed to air")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __addr_str(cls, addr):
        if addr is None:
            return None

        return "0x%02x" % addr


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def int_addr(self):
        return self.__opts.int_addr


    @property
    def ext_addr(self):
        return self.__opts.ext_addr


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CmdSHTConf:{int_addr:%s, ext_addr:%s, verbose:%s, args:%s}" % \
                    (CmdSHTConf.__addr_str(self.int_addr), CmdSHTConf.__addr_str(self.ext_addr), self.verbose,
                     self.args)
