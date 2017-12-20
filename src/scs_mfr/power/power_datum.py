"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PowerDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, amps, volts):
        """
        Constructor
        """
        watts = amps * volts

        self.__amps = Datum.float(amps, 3)
        self.__volts = Datum.float(volts, 3)
        self.__watts = Datum.float(watts, 3)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['amp'] = self.amps
        jdict['vlt'] = self.volts
        jdict['wtt'] = self.watts

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def amps(self):
        return self.__amps


    @property
    def volts(self):
        return self.__volts


    @property
    def watts(self):
        return self.__watts


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PowerDatum:{amps:%0.3f, volts:%0.3f, watts:%0.3f}" % (self.amps, self.volts, self.watts)
