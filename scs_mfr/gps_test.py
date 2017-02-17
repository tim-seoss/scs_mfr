#!/usr/bin/env python3

"""
Created on 4 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.location.gpgsa import GPGSA
from scs_core.location.gprmc import GPRMC
from scs_core.sync.sampler import Sampler

from scs_dfe.gps.pam7q import PAM7Q

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class GPSSampler(Sampler):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gps_module, interval, sample_count=0):
        """
        Constructor
        """
        Sampler.__init__(self, interval, sample_count)

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
        # resource...

        print("power on...")
        gps.power_on()

        gps_sampler = GPSSampler(gps, 10)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        start = time.time()
        prev_gpgsa = None
        gpmrc = None

        for gpgsa in gps_sampler.samples():

            if gpgsa != prev_gpgsa:
                print(gpgsa)

            prev_gpgsa = gpgsa

            gps.open()
            gpmrc = gps.report(GPRMC)
            gps.close()

            if gpmrc is not None and gpmrc.has_position():
                break


        # ------------------------------------------------------------------------------------------------------------
        # report...

        print("position: %s, %s  time: %s" % (gpmrc.loc.deg_lat(), gpmrc.loc.deg_lng(), gpmrc.datetime.as_iso8601()))

        elapsed = int(time.time() - start)
        print("elapsed: %ds" % elapsed)

        print("-")


    except KeyboardInterrupt as ex:
        print("pamq7_test: " + type(ex).__name__)


        # ----------------------------------------------------------------------------------------------------------------

    finally:
        # print("power down...")
        # gps.power_off()

        I2C.close()
