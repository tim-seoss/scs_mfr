"""
Created on 13 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdOPCFirmwareConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [-s FIELD VALUE] [-c] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--set", "-s", type="string", nargs=2, action="store", dest="set",
                                 help="set FIELD to integer VALUE")

        self.__parser.add_option("--commit", "-c", action="store_true", dest="commit", default=False,
                                 help="commit the configuration to non-volatile memory")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.set is not None:
            try:
                int(self.__opts.set[1])
            except ValueError:
                return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def set_field(self):
        return None if self.__opts.set is None else self.__opts.set[0]


    @property
    def set_value(self):
        return None if self.__opts.set is None else int(self.__opts.set[1])


    @property
    def commit(self):
        return self.__opts.commit


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdOPCConf:{set:%s, commit:%s, verbose:%s}" % (self.__opts.set, self.__opts.commit, self.verbose)
