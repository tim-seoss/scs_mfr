"""
Created on 29 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdSchedule(object):
    """unix command line handler"""

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{-s NAME INTERVAL TALLY | -c NAME }] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--set", "-s", type="string", nargs=3, action="store", dest="set",
                                 help="set schedule NAME, INTERVAL (float) and TALLY (int)")

        self.__parser.add_option("--delete", "-d", type="string", nargs=1, action="store", dest="delete",
                                 help="delete the named schedule")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.clear():
            return False

        if self.set():
            try:
                float(self.__opts.set[1])
                int(self.__opts.set[2])

            except ValueError:
                return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.__opts.set is not None


    def delete(self):
        return self.__opts.clear is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        if self.__opts.set is not None:
            return self.__opts.set[0]

        if self.__opts.clear is not None:
            return self.__opts.clear

        return None


    @property
    def interval(self):
        return None if self.__opts.set is None else self.__opts.set[1]


    @property
    def count(self):
        return None if self.__opts.set is None else self.__opts.set[2]


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
        return "CmdSchedule:{name:%s, interval:%s, count:%s, verbose:%s, args:%s}" % \
                    (self.name, self.interval, self.count, self.verbose, self.args)
