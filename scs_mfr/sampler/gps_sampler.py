"""
Created on 30 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.location.gpgsa import GPGSA
from scs_core.sampler.sampler import Sampler


# --------------------------------------------------------------------------------------------------------------------

class GPSSampler(Sampler):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, runner, gps_module):
        """
        Constructor
        """
        Sampler.__init__(self, runner)

        self.__gps = gps_module


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        self.__gps.open()
        sample = self.__gps.report(GPGSA)
        self.__gps.close()

        return sample


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSSampler:{runner:%s, gps:%s}" % (self.runner, self.__gps)
