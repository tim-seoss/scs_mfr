"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdPSUConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{-m { PrototypeV1 | OsloV1 } | -r}] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--model", "-m", type="string", nargs=1, action="store", dest="model",
                                 help="set PSU model")

        self.__parser.add_option("--remove", "-r", action="store_true", dest="remove", default=False,
                                 help="remove PSU model")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.remove and self.__opts.model is not None:
            return False

        if self.__opts.model is not None and self.__opts.model != 'PrototypeV1' and self.__opts.model != 'OsloV1':
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.__opts.remove or self.__opts.model is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        if self.__opts.remove:
            return None

        return self.__opts.model


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
        return "CmdPSUConf:{model:%s, verbose:%s, args:%s}" % (self.model, self.verbose, self.args)
