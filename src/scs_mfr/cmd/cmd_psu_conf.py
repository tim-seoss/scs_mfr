"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

class CmdPSUConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        models = ' | '.join(PSUConf.models())

        self.__parser = optparse.OptionParser(usage="%prog [{ -m MODEL | -d }] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--model", "-m", type="string", nargs=1, action="store", dest="model",
                                 help="set PSU model { %s }" % models)

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the PSU configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.model is not None and self.delete:
            return False

        if self.set() and self.model not in PSUConf.models():
            return False

        return True


    def set(self):
        return self.__opts.model


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__opts.model


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
        return "CmdPSUConf:{model:%s, delete:%s, verbose:%s}" % (self.model, self.delete, self.verbose)
