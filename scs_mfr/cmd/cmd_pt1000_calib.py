"""
Created on 28 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdPt1000Calib(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--set", "-s", action="store_true", dest="set", default=False,
                                 help="set Pt1000 calib from internal SHT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def set(self):
        return self.__opts.set


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CmdPt1000Calib:{set:%s, verbose:%s, args:%s}" % (self.set, self.verbose, self.args)
