"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdOSIOPublication(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s LOCATION DEVICE] [-v]",
                                              version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--set", "-s", type="string", nargs=2, action="store", dest="location_device",
                                 help="paths for location and device topics")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.__opts.location_device is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def location_path(self):
        return self.__opts.location_device[0] if self.__opts.location_device else None


    @property
    def device_path(self):
        return self.__opts.location_device[1] if self.__opts.location_device else None


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CmdOSIOPublication:{location_path:%s, device_path:%s, verbose:%s, args:%s}" % \
               (self.location_path, self.device_path, self.verbose, self.args)
