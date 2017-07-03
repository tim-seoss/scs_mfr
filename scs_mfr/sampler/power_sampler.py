"""
Created on 30 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sampler.sampler import Sampler

from scs_mfr.power.power_meter import PowerMeter


# --------------------------------------------------------------------------------------------------------------------

class PowerSampler(Sampler):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, runner):
        """
        Constructor
        """
        Sampler.__init__(self, runner)

        self.__meter = PowerMeter()
        self.__meter.reset()

        self.reset()


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        return 'pow', self.__meter.sample


    def close(self):
        self.__meter.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PowerSampler:{runner:%s, meter:%s}" % (self.runner, self.__meter)
