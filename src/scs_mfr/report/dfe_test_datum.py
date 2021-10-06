"""
Created on 29 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class DFETestDatum(Sample):
    """
    classdocs
    """

    VERSION = 1.0

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, host_serial_number, dfe_serial_number, subjects, afe, result, version=None):
        """
        Constructor
        """
        if version is None:
            version = self.VERSION

        super().__init__(tag, rec, version)

        self.__host_serial_number = host_serial_number                  # string
        self.__dfe_serial_number = dfe_serial_number                    # string
        self.__subjects = subjects                                      # dict of string: string
        self.__afe = afe                                                # HostStatus
        self.__result = result                                          # string


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def has_invalid_value(cls):
        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def values(self):
        jdict = OrderedDict()

        jdict['host-sn'] = self.host_serial_number
        jdict['dfe-sn'] = self.dfe_serial_number
        jdict['result'] = self.result
        jdict['subjects'] = self.subjects
        jdict['afe'] = self.afe

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def host_serial_number(self):
        return self.__host_serial_number


    @property
    def dfe_serial_number(self):
        return self.__dfe_serial_number


    @property
    def subjects(self):
        return self.__subjects


    @property
    def afe(self):
        return self.__afe


    @property
    def result(self):
        return self.__result


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "StatusSample:{tag:%s, rec:%s, src:%s, host_serial_number:%s, dfe_serial_number:%s, " \
               "subjects:%s,  afe:%s, result:%s}" % \
            (self.tag, self.rec, self.src, self.host_serial_number, self.dfe_serial_number,
             self.subjects, self.afe, self.result)
