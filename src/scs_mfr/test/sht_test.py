"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_host.bus.i2c import I2C

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class SHTTest(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, sht, interface, verbose):
        super().__init__(interface, verbose)

        self.__name = name
        self.__sht = sht


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self, ):
        if self.verbose:
            print("%s (0x%02x)..." % (self.__name, self.__sht.addr), file=sys.stderr)

        try:
            I2C.Sensors.open()

            # test...
            self.__sht.reset()

            self._datum = self.__sht.sample()

            if self.verbose:
                print(self._datum, file=sys.stderr)

            # criterion...
            return 10 < self._datum.humid < 90 and 10 < self._datum.temp < 50

        finally:
            I2C.Sensors.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SHTTest:{name:%s, sht:%s, datum:%s, interface:%s, verbose:%s}" % \
               (self.__name, self.__sht, self.datum, self.__interface, self.__verbose)
