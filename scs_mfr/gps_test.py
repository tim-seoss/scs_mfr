#!/usr/bin/env python3

"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.location.gpgga import GPGGA
from scs_core.location.gpgsa import GPGSA
from scs_core.location.gprmc import GPRMC
from scs_core.location.gps_location import GPSLocation

from scs_core.sync.timed_runner import TimedRunner

from scs_dfe.gps.pam7q import PAM7Q

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class GPSSampler(TimedRunner):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gps_module, interval, sample_count=None):
        """
        Constructor
        """
        TimedRunner.__init__(self, interval, sample_count)

        self.__gps = gps_module


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        self.__gps.open()
        sample = self.__gps.report(GPGSA)
        self.__gps.close()

        return sample


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSSampler:{gps:%s}" % self.__gps


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    I2C.open(Host.I2C_SENSORS)

    gps = PAM7Q()

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        print("power on...")
        gps.power_on()

        gps_sampler = GPSSampler(gps, 10)

        print(gps_sampler, file=sys.stderr)
        sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        start = time.time()
        prev_gsa = None
        rmc = None

        for gsa in gps_sampler.samples():
            if gsa != prev_gsa:
                print(gsa)

            prev_gsa = gsa

            gps.open()
            rmc = gps.report(GPRMC)
            gps.close()

            if rmc is not None and rmc.has_position():
                break


        # ------------------------------------------------------------------------------------------------------------
        # report...

        elapsed = int(time.time() - start)

        gps.open()
        gga = gps.report(GPGGA)
        gps.close()

        loc = GPSLocation.construct(gga)


        print("time: %s" % rmc.datetime.as_iso8601())
        print(loc)
        print("elapsed: %ds" % elapsed)

        print("-")


    except KeyboardInterrupt as ex:
        print("pamq7_test: " + type(ex).__name__)


        # ----------------------------------------------------------------------------------------------------------------

    finally:
        # print("power down...")
        # gps.power_off()

        I2C.close()
