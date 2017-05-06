"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdAFEBaseline(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-1 SN1_OFFSET] [-2 SN2_OFFSET] [-3 SN3_OFFSET] "
                                                    "[-4 SN3_OFFSET] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--sn1", "-1", type="int", nargs=1, action="store", dest="sn1_offset",
                                 help="SN1 baseline offset")

        self.__parser.add_option("--sn2", "-2", type="int", nargs=1, action="store", dest="sn2_offset",
                                 help="SN2 baseline offset")

        self.__parser.add_option("--sn3", "-3", type="int", nargs=1, action="store", dest="sn3_offset",
                                 help="SN3 baseline offset")

        self.__parser.add_option("--sn4", "-4", type="int", nargs=1, action="store", dest="sn4_offset",
                                 help="SN4 baseline offset")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.__opts.sn1_offset is not None or self.__opts.sn2_offset is not None or \
               self.__opts.sn3_offset is not None or self.__opts.sn4_offset is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def offsets(self):
        return {0: self.sn1_offset, 1: self.sn2_offset, 2: self.sn3_offset, 3: self.sn4_offset}


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sn1_offset(self):
        return self.__opts.sn1_offset


    @property
    def sn2_offset(self):
        return self.__opts.sn2_offset


    @property
    def sn3_offset(self):
        return self.__opts.sn3_offset


    @property
    def sn4_offset(self):
        return self.__opts.sn4_offset


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CmdAFEBaseline:{sn1_offset:%s, sn2_offset:%s, sn3_offset:%s, sn4_offset:%s, verbose:%s, args:%s}" % \
               (self.sn1_offset, self.sn2_offset, self.sn3_offset, self.sn4_offset, self.verbose, self.args)
