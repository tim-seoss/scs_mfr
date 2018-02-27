"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdGPSConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{ -m MODEL | -d }] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--model", "-m", action="store_true", dest="model",
                                 help="set MODEL (must be PAM7Q)")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete",
                                 help="delete the GPS configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.model is not None and self.delete:
            return False

        return True


    def set(self):
        return self.__opts.model


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        model = self.__args[0] if len(self.__args) > 0 else None

        return model if self.__opts.model else None


    @property
    def delete(self):
        return self.__opts.delete


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
        return "CmdGPSConf:{model:%s, delete:%s, verbose:%s, args:%s}" % \
               (self.model, self.delete, self.verbose, self.args)
