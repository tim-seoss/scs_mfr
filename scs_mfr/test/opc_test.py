"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_dfe.particulate.opc_n2 import OPCN2


# --------------------------------------------------------------------------------------------------------------------

class OPCTest(object):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def conduct(cls, verbose):
        if verbose:
            print("OPC...", file=sys.stderr)

        opc = None

        try:
            opc = OPCN2()
            opc.power_on()
            opc.operations_on()

            firmware = opc.firmware()

            if verbose:
                print(firmware, file=sys.stderr)

            # test criterion...
            return len(firmware) > 0

        finally:
            if opc:
                opc.operations_off()
                opc.power_off()
