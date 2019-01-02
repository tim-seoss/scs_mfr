"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_dfe.gps.pam7q import PAM7Q


# --------------------------------------------------------------------------------------------------------------------

class CmdGPSConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{ [-m MODEL] [-i INTERVAL] [-t TALLY] | -d }] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--model", "-m", type="string", nargs=1, action="store", dest="model",
                                 help="set the model (must be PAM7Q)")

        self.__parser.add_option("--sample-interval", "-i", type="int", nargs=1, action="store", dest="sample_interval",
                                 help="set sampling interval")

        self.__parser.add_option("--tally", "-t", type="int", nargs=1, action="store", dest="tally",
                                 help="set the averaging tally")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete",
                                 help="delete the GPS configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.model and self.model != PAM7Q.SOURCE:
            return False

        return True


    def is_complete(self):
        if self.model is None or self.sample_interval is None or self.tally is None:
            return False

        return True


    def set(self):
        return self.model is not None or self.sample_interval is not None or self.tally is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__opts.model


    @property
    def sample_interval(self):
        return self.__opts.sample_interval


    @property
    def tally(self):
        return self.__opts.tally


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
        return "CmdGPSConf:{model:%s, sample_interval:%s, tally:%s, delete:%s, verbose:%s, args:%s}" % \
               (self.model, self.sample_interval, self.tally, self.delete, self.verbose, self.args)
