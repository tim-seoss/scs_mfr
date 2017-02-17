"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdDeviceID(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s MODEL CONFIG SERIAL] [-v]",
                                              version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--set", "-s", type="string", nargs=3, action="store", dest="model_config_serial",
                                 help="SERIAL must be an integer")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.__opts.model_config_serial is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__opts.model_config_serial[0] if self.__opts.model_config_serial else None


    @property
    def configuration(self):
        return self.__opts.model_config_serial[1].upper() if self.__opts.model_config_serial else None


    @property
    def serial_number(self):
        return int(self.__opts.model_config_serial[2]) if self.__opts.model_config_serial else None


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CmdDeviceID:{model:%s, configuration:%s, serial_number:%s, verbose:%s, args:%s}" % \
               (self.model, self.configuration, self.serial_number, self.verbose, self.args)
