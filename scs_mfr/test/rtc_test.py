"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time
import tzlocal

from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.data.rtc_datetime import RTCDatetime

from scs_dfe.time.ds1338 import DS1338


# --------------------------------------------------------------------------------------------------------------------

class RTCTest(object):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def conduct(cls, verbose):
        if verbose:
            print("RTC...", file=sys.stderr)

        now = LocalizedDatetime.now()

        DS1338.init()

        rtc_datetime = RTCDatetime.construct_from_localized_datetime(now)
        DS1338.set_time(rtc_datetime)

        time.sleep(2)

        rtc_datetime = DS1338.get_time()
        localized_datetime = rtc_datetime.as_localized_datetime(tzlocal.get_localzone())

        diff = localized_datetime - now

        # test criterion...
        return diff.seconds >= 1
