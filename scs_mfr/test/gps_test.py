"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.location.gprmc import GPRMC

from scs_dfe.gps.pam7q import PAM7Q


# --------------------------------------------------------------------------------------------------------------------

class GPSTest(object):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def conduct(cls, verbose):
        if verbose:
            print("GPS...", file=sys.stderr)

        gps = None
        
        try:
            gps = PAM7Q()
            gps.power_on()
            gps.open()

            msg = gps.report(GPRMC)

            if verbose:
                print(msg, file=sys.stderr)

            # test criterion...
            return msg is not None

        finally:
            if gps:
                gps.close()
                gps.power_off()
