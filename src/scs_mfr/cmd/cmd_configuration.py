"""
Created on 29 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdConfiguration(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s CONFIGURATION] [-i INDENT] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--save", "-s", type="string", nargs=1, action="store", dest="configuration",
                                 help="save the given JSON configuration component(s)")

        # output...
        self.__parser.add_option("--indent", "-i", action="store", dest="indent", type=int,
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def save(self):
        return self.__opts.configuration is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def configuration(self):
        return self.__opts.configuration


    @property
    def indent(self):
        return self.__opts.indent


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdConfiguration:{configuration:%s, indent:%s, verbose:%s}" % \
               (self.configuration, self.indent, self.verbose)
