"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.location.gprmc import GPRMC

from scs_dfe.gps.pam7q import PAM7Q

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class GPSTest(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose):
        Test.__init__(self, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("GPS...", file=sys.stderr)

        gps = None
        
        try:
            # resources...
            gps = PAM7Q()
            gps.power_on()
            gps.open()

            # test...
            msg = gps.report(GPRMC)

            if self.verbose:
                print(msg, file=sys.stderr)

            # criterion...
            return msg is not None

        finally:
            if gps:
                gps.close()
                gps.power_off()
