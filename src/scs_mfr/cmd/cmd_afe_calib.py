"""
Created on 27 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from datetime import date


# --------------------------------------------------------------------------------------------------------------------

class CmdAFECalib(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{-a AFE_SERIAL_NUMBER | "
                                                    "-s A4_SERIAL_NUMBER YYYY-MM-DD WE_SENS WE_X_SENS | "
                                                    "-t}] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--afe", "-a", type="string", nargs=1, action="store", dest="afe_serial_number",
                                 help="set AFE serial number")

        self.__parser.add_option("--dsi", "-s", type="string", nargs=4, action="store", dest="dsi",
                                 help="set DSI serial number, calibration date, We sens mV, We cross-sens mV")

        self.__parser.add_option("--test", "-t", action="store_true", dest="test", default=False,
                                 help="set AFE to test load")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.afe_serial_number is not None:
            count += 1

        if self.dsi is not None:
            count += 1

        if self.test:
            count += 1

        if count > 1:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.afe_serial_number is not None or self.dsi is not None or self.test


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def afe_serial_number(self):
        return self.__opts.afe_serial_number


    @property
    def dsi(self):
        return self.__opts.dsi


    @property
    def dsi_serial_number(self):
        return None if self.__opts.dsi is None else self.__opts.dsi[0]


    @property
    def dsi_calibration_date_str(self):
        return None if self.__opts.dsi is None else self.__opts.dsi[1]


    @property
    def dsi_calibration_date(self):
        if self.__opts.dsi is None:
            return None

        pieces = self.__opts.dsi[1].split('-')
        return date(int(pieces[0]), int(pieces[1]), int(pieces[2]))


    @property
    def dsi_we_sens_mv_str(self):
        return None if self.__opts.dsi is None else self.__opts.dsi[2]


    @property
    def dsi_we_sens_mv(self):
        return None if self.__opts.dsi is None else float(self.__opts.dsi[2])


    @property
    def dsi_we_no2_x_sens_mv(self):
        if self.__opts.dsi is None:
            return None

        try:
            return float(self.__opts.dsi[3])
        except ValueError:
            return "n/a"


    @property
    def test(self):
        return self.__opts.test


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdAFECalib:{afe_serial_number:%s, dsi:%s, test:%s, verbose:%s}" % \
               (self.afe_serial_number, self.dsi, self.test, self.verbose)
