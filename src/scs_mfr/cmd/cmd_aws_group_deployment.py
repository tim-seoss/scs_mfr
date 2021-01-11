"""
Created on 11 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CMDAWSDeployment(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-i INDENT] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--indent", "-i", action="store", dest="indent", type=int,
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()

    # ----------------------------------------------------------------------------------------------------------------


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
        return "CMDAWSDeployment:{indent:%s verbose:%s}" % (self.indent, self.verbose)
