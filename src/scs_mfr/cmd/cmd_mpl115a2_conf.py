"""
Created on 21 Jun 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdMPL115A2Conf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{ -a ALTITUDE | -d }] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--altitude", "-a", type="string", nargs=1, action="store", dest="altitude",
                                 help="altitude in metres or 'auto' for GPS altitude")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the MPL115A2 configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.altitude is None or self.altitude == 'auto':
            return True

        try:
            int(self.altitude)
        except ValueError:
            return False

        return True


    def set(self):
        return self.__opts.altitude is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def altitude(self):
        try:
            return int(self.__opts.altitude)
        except (TypeError, ValueError):
            return self.__opts.altitude


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
        return "CmdMPL115A2Conf:{altitude:%s, delete:%s, verbose:%s, args:%s}" % \
               (self.altitude, self.delete, self.verbose, self.args)
