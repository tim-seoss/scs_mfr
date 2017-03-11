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
        self.__parser = optparse.OptionParser(usage="%prog [-s VENDOR_ID MODEL_ID MODEL_NAME CONFIG SERIAL] [-v]",
                                              version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--set", "-s", type="string", nargs=5, action="store", dest="model_config_serial",
                                 help="SERIAL is normally integer")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.__opts.model_config_serial is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def vendor_id(self):
        return self.__opts.model_config_serial[0] if self.__opts.model_config_serial else None


    @property
    def model_id(self):
        return self.__opts.model_config_serial[1] if self.__opts.model_config_serial else None


    @property
    def model_name(self):
        return self.__opts.model_config_serial[2] if self.__opts.model_config_serial else None


    @property
    def configuration(self):
        return self.__opts.model_config_serial[3] if self.__opts.model_config_serial else None


    @property
    def serial_number(self):
        return self.__opts.model_config_serial[4] if self.__opts.model_config_serial else None


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CmdDeviceID:{vendor_id:%s, model_id:%s, model_name:%s, " \
               "configuration:%s, serial_number:%s, verbose:%s, args:%s}" % \
               (self.vendor_id, self.model_id, self.model_name,
                self.configuration, self.serial_number, self.verbose, self.args)
