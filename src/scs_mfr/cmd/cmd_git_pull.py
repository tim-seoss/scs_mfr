"""
Created on 24 Feb 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdGitPull(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-p [-t TIMEOUT]] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--pull", "-p", action="store_true", dest="pull", default=False,
                                 help="perform a git pull")

        self.__parser.add_option("--timeout", "-t", type="int", nargs=1, action="store", dest="timeout", default=10,
                                 help="timeout for each pull (default 10 seconds)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pull(self):
        return self.__opts.pull


    @property
    def timeout(self):
        return self.__opts.timeout


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CmdGitPull:{pull:%s, timeout:%s, verbose:%s}" % (self.pull, self.timeout, self.verbose)
