"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class SHTTest(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, sht, verbose):
        Test.__init__(self, verbose)

        self.__name = name
        self.__sht = sht


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self, ):
        if self.verbose:
            print("%s (0x%02x)..." % (self.__name, self.__sht.addr), file=sys.stderr)

        try:
            I2C.open(Host.I2C_SENSORS)

            # test...
            self.__sht.reset()
            int_sht_datum = self.__sht.sample()

            if self.verbose:
                print(int_sht_datum, file=sys.stderr)

            humid = int_sht_datum.humid
            temp = int_sht_datum.temp

            # criterion...
            return 10 < humid < 90 and 10 < temp < 50

        finally:
            I2C.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SHTTest:{name:%s, sht:%s, datum:%s, verbose:%s}" % \
               (self.__name, self.__sht, self.datum, self.__verbose)
