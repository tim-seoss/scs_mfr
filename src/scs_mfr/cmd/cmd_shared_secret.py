"""
Created on 2 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"org-id": "south-coast-science-test-user", "api-key": "9fdfb841-3433-45b8-b223-3f5a283ceb8e"}
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdSharedSecret(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ -g | -d }] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--generate", "-g", action="store_true", dest="generate", default=False,
                                 help="set shared secret")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the shared secret")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.generate and self.delete:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def generate(self):
        return self.__opts.generate


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
        return "CmdSharedSecret:{generate:%s, delete:%s, verbose:%s, args:%s}" % \
               (self.generate, self.delete, self.verbose, self.args)
