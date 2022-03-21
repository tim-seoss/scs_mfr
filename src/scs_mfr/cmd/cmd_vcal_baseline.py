"""
Created on 10 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class CmdVCalBaseline(object):
    """unix command line handler"""


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __is_integer(value):
        try:
            int(value)
        except ValueError:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ -b GAS  | { -s GAS VALUE | -c GAS MINIMUM } "
                                                    "[-r SAMPLE_REC -t SAMPLE_TEMP -m SAMPLE_HUMID] "
                                                    "| -d }] [-v]", version="%prog 1.0")

        # functions...
        self.__parser.add_option("--baseline", "-b", type="string", nargs=1, action="store", dest="baseline",
                                 help="report offset for GAS")

        self.__parser.add_option("--set", "-s", type="string", nargs=2, action="store", dest="set",
                                 help="set offset for GAS to integer VALUE")

        self.__parser.add_option("--match-compendium", "-c", type="string", nargs=2, action="store", dest="match",
                                 help="set offset for GAS to match MINIMUM of the compendium")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the baseline configuration")

        # sample...
        self.__parser.add_option("--sample-rec", "-r", type="string", nargs=1, action="store", dest="sample_rec",
                                 help="sample ISO 8601 datetime")

        self.__parser.add_option("--sample-temp", "-t", type="float", nargs=1, action="store", dest="sample_temp",
                                 help="sample temperature")

        self.__parser.add_option("--sample-humid", "-m", type="float", nargs=1, action="store", dest="sample_humid",
                                 help="sample humidity")

        # output...
        self.__parser.add_option("--indent", "-i", action="store", dest="indent", type=int,
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        # commands...
        if self.baseline is not None:
            count += 1

        if self.set is not None:
            count += 1

        if self.match is not None:
            count += 1

        if self.delete:
            count += 1

        if count > 1:
            return False

        # sample...
        count = 0

        if self.__opts.sample_rec is not None:
            count += 1

        if self.__opts.sample_temp is not None:
            count += 1

        if self.__opts.sample_humid is not None:
            count += 1

        if count != 0 and count != 3:
            return False

        if count == 3 and not self.set and not self.match:
            return False

        # VALUE...
        if self.set is not None and not self.__is_integer(self.set[1]):
            return False

        if self.match is not None and not self.__is_integer(self.match[1]):
            return False

        return True


    def is_valid_sample_rec(self):
        if self.__opts.sample_rec is None:
            return True

        return self.sample_rec is not None


    # ----------------------------------------------------------------------------------------------------------------

    def gas_name(self):
        if self.baseline:
            return self.baseline

        if self.set:
            return self.set[0]

        if self.match:
            return self.match[0]

        return None


    def update(self):
        return self.set is not None or self.match is not None


    def has_sample(self):
        return self.__opts.sample_rec is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def baseline(self):
        return self.__opts.baseline


    @property
    def set(self):
        return self.__opts.set


    def set_value(self):
        return None if self.set is None else int(self.set[1])


    @property
    def match(self):
        return self.__opts.match


    def match_value(self):
        return None if self.match is None else int(self.match[1])


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def sample_rec(self):
        return LocalizedDatetime.construct_from_iso8601(self.__opts.sample_rec)


    @property
    def sample_temp(self):
        return self.__opts.sample_temp


    @property
    def sample_humid(self):
        return self.__opts.sample_humid


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
        return "CmdVCalBaseline:{baseline:%s, set:%s, match:%s, delete:%s, " \
               "sample_rec:%s, sample_temp:%s, sample_humid:%s, indent:%s, verbose:%s}" % \
               (self.baseline, self.set, self.match, self.delete,
                self.sample_rec, self.sample_temp, self.sample_humid, self.indent, self.verbose)
