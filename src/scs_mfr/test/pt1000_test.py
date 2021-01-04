"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class Pt1000Test(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface, verbose):
        super().__init__(interface, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("Pt1000...", file=sys.stderr)

        try:
            I2C.Sensors.open()

            # AFE...
            if self.interface.pt1000(Host) is None:
                print("No Pt1000 I2C address set - skipping.", file=sys.stderr)
                return False

            afe = self.interface.gas_sensors(Host)

            # test...
            self._datum = afe.sample_pt1000()

            if self.verbose:
                print(self._datum, file=sys.stderr)

            # test criterion...
            return 0.3 < self._datum.v < 0.4

        finally:
            I2C.Sensors.close()
