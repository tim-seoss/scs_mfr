"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.gas.pt1000_calib import Pt1000Calib
from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib

from scs_dfe.gas.afe import AFE
from scs_dfe.gas.pt1000 import Pt1000
from scs_dfe.gas.pt1000_conf import Pt1000Conf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class AFETest(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose):
        Test.__init__(self, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("AFE...", file=sys.stderr)

        try:
            I2C.open(Host.I2C_SENSORS)

            # Pt1000...
            pt1000_conf = Pt1000Conf.load_from_host(Host)
            pt1000_calib = Pt1000Calib.load_from_host(Host)
            pt1000 = Pt1000(pt1000_calib)

            # AFE...
            afe_baseline = AFEBaseline.load_from_host(Host)

            afe_calib = AFECalib.load_from_host(Host)
            sensors = afe_calib.sensors(afe_baseline)

            afe = AFE(pt1000_conf, pt1000, sensors)

            # test...
            self.datum = afe.sample()

            if self.verbose:
                print(self.datum, file=sys.stderr)

            ok = True

            # test criterion...
            for gas, sensor in self.datum.sns.items():
                # noinspection PyTypeChecker,PyTypeChecker
                sensor_ok = 0.9 < sensor.we_v < 1.1 and 0.9 < sensor.ae_v < 1.1

                if not sensor_ok:
                    ok = False

            return ok

        finally:
            I2C.close()
