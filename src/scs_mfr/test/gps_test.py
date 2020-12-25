"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.position.nmea.gprmc import GPRMC

from scs_dfe.gps.pam_7q import PAM7Q

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class GPSTest(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface, verbose):
        super().__init__(interface, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("GPS...", file=sys.stderr)

        gps = None

        try:
            I2C.Sensors.open()

            # GPS...
            gps = PAM7Q(self.interface, Host.gps_device())

            gps.power_on()
            gps.open()

            # test...
            self._datum = gps.report(GPRMC)

            if self.verbose:
                print(self._datum, file=sys.stderr)

            # criterion...
            return self._datum is not None

        finally:
            if gps:
                gps.close()
                gps.power_off()

            I2C.Sensors.close()
