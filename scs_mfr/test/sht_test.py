"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys


# --------------------------------------------------------------------------------------------------------------------

class SHTTest(object):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def conduct(cls, name, sht, verbose):
        if verbose:
            print("%s (0x%02x)..." % (name, sht.addr), file=sys.stderr)

        sht.reset()
        int_sht_datum = sht.sample()

        if verbose:
            print(int_sht_datum, file=sys.stderr)

        humid = int_sht_datum.humid
        temp = int_sht_datum.temp

        # test criterion...
        return 10 < humid < 90 and 10 < temp < 50
