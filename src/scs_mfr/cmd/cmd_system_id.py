"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdSystemID(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-d VENDOR_ID] [-m MODEL_ID] [-n MODEL_NAME] [-c CONFIG] "
                                                    "[-s SYSTEM_SERIAL_NUMBER] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--vendor", "-d", type="string", nargs=1, action="store", dest="vendor_id",
                                 help="set vendor ID (required if there is no current record)")

        self.__parser.add_option("--model", "-m", type="string", nargs=1, action="store", dest="model_id",
                                 help="set model ID (required if there is no current record)")

        self.__parser.add_option("--name", "-n", type="string", nargs=1, action="store", dest="model_name",
                                 help="set model name (required if there is no current record)")

        self.__parser.add_option("--config", "-c", type="string", nargs=1, action="store", dest="configuration",
                                 help="set device configuration (required if there is no current record)")

        self.__parser.add_option("--serial", "-s", type="int", nargs=1, action="store", dest="serial_number",
                                 help="set serial number (required if there is no current record)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()



    # ----------------------------------------------------------------------------------------------------------------

    def is_complete(self):
        if self.vendor_id is None or self.model_id is None or self.model_name is None or \
                        self.configuration is None or self.serial_number is None:
            return False

        return True


    def set(self):
        if self.vendor_id is not None or self.model_id is not None or self.model_name is not None or \
                        self.configuration is not None or self.serial_number is not None:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def vendor_id(self):
        return self.__opts.vendor_id


    @property
    def model_id(self):
        return self.__opts.model_id


    @property
    def model_name(self):
        return self.__opts.model_name


    @property
    def configuration(self):
        return self.__opts.configuration


    @property
    def serial_number(self):
        return self.__opts.serial_number


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
        return "CmdSystemID:{vendor_id:%s, model_id:%s, model_name:%s, " \
               "configuration:%s, serial_number:%s, verbose:%s, args:%s}" % \
               (self.vendor_id, self.model_id, self.model_name,
                self.configuration, self.serial_number, self.verbose, self.args)
