"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.gas.pt1000_calib import Pt1000Calib

from scs_dfe.gas.afe import AFE
from scs_dfe.gas.pt1000 import Pt1000
from scs_dfe.gas.pt1000_conf import Pt1000Conf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class Pt1000Test(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose):
        Test.__init__(self, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("Pt1000...", file=sys.stderr)

        try:
            I2C.open(Host.I2C_SENSORS)

            # resources...
            pt1000_conf = Pt1000Conf.load_from_host(Host)
            pt1000_calib = Pt1000Calib.load_from_host(Host)
            pt1000 = Pt1000(pt1000_calib)

            afe = AFE(pt1000_conf, pt1000, [])

            # test...
            self.datum = afe.sample_temp()

            if self.verbose:
                print(self.datum, file=sys.stderr)

            # test criterion...
            # noinspection PyTypeChecker
            return 0.4 < self.datum.v < 0.6

        finally:
            I2C.close()
