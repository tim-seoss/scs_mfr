"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class OPCTest(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface, verbose):
        Test.__init__(self, interface, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("OPC...", file=sys.stderr)

        opc = None

        try:
            I2C.open(Host.I2C_SENSORS)

            # resources...
            opc_conf = OPCConf.load(Host)

            if opc_conf is None:
                print("OPCConf not available - skipping.", file=sys.stderr)
                return False

            opc = opc_conf.opc(Host, False)

            self._interface.power_opc(True)
            opc.operations_on()

            # test...
            self._datum = opc.firmware()

            if self.verbose:
                print(self._datum, file=sys.stderr)

            # test criterion...
            return len(self._datum) > 0 and self._datum.startswith('OPC')

        finally:
            if opc:
                opc.operations_off()
                self._interface.power_opc(False)

            I2C.close()
