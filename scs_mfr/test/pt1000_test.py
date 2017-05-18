"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_dfe.board.mcp9808 import MCP9808


# --------------------------------------------------------------------------------------------------------------------

class Pt1000Test(object):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def conduct(cls, verbose):
        if verbose:
            print("Pt1000...", file=sys.stderr)

        # TODO: implement Pt1000Test

        sensor = MCP9808(True)

        datum = sensor.sample()

        if verbose:
            print(datum, file=sys.stderr)

        temp = datum.temp

        # test criterion...
        return 10 < temp < 50
