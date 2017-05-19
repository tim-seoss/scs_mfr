"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_dfe.board.mcp9808 import MCP9808

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class BoardTempTest(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose):
        Test.__init__(self, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("Board temp...", file=sys.stderr)

        try:
            I2C.open(Host.I2C_SENSORS)

            # resources...
            sensor = MCP9808(True)

            # test...
            self.datum = sensor.sample()

            if self.verbose:
                print(self.datum, file=sys.stderr)

            temp = self.datum.temp

            # test criterion...
            return 10 < temp < 50

        finally:
            I2C.close()
