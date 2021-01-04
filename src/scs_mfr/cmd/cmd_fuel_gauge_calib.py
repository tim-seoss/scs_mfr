"""
Created on 4 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdFuelGaugeCalib(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { { -n | -l { D | F } | -s } | "
                                                    "{ -c | -f | -p } [-i INTERVAL] } "
                                                    "[-v]", version="%prog 1.0")

        # single shot...
        self.__parser.add_option("--initialise", "-n", action="store_true", dest="initialise", default=False,
                                 help="initialise the fuel gauge configuration")

        self.__parser.add_option("--load", "-l", type="string", nargs=1, action="store", dest="load",
                                 help="load fuel gauge parameters from Default or Filesystem")

        self.__parser.add_option("--save", "-s", action="store_true", dest="save", default=False,
                                 help="save the current fuel gauge parameters to filesystem")

        # iterable...
        self.__parser.add_option("--current", "-c", action="store_true", dest="current", default=False,
                                 help="report the current fuel gauge parameters")

        self.__parser.add_option("--fuel", "-f", action="store_true", dest="fuel", default=False,
                                 help="sample the fuel gauge")

        self.__parser.add_option("--power", "-p", action="store_true", dest="power", default=False,
                                 help="sample the PSU")

        # optional...
        self.__parser.add_option("--interval", "-i", type="float", nargs=1, action="store", dest="interval",
                                 help="sampling interval in seconds")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.initialise:
            count += 1

        if self.load:
            count += 1

        if self.save:
            count += 1

        if self.current:
            count += 1

        if self.fuel:
            count += 1

        if self.power:
            count += 1

        if count != 1:
            return False

        if self.load and self.load not in ('D', 'F'):
            return False

        if (self.initialise or self.load or self.save) and self.interval:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def initialise(self):
        return self.__opts.initialise


    @property
    def load(self):
        return self.__opts.load


    @property
    def save(self):
        return self.__opts.save


    @property
    def current(self):
        return self.__opts.current


    @property
    def fuel(self):
        return self.__opts.fuel


    @property
    def power(self):
        return self.__opts.power


    @property
    def interval(self):
        return 0 if self.__opts.interval is None else self.__opts.interval


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdFuelGaugeCalib:{initialise:%s, load:%s, save:%s, " \
               "current:%s, fuel:%s, power:%s, interval:%s, verbose:%s}" % \
               (self.initialise, self.load, self.save,
                self.current, self.fuel, self.power, self.interval, self.verbose)
