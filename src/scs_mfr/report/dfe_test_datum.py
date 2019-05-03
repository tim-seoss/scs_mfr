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

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, host_serial_number, dfe_serial_number, subjects, afe, result):
        """
        Constructor
        """
        jdict = OrderedDict()

        jdict['host-sn'] = host_serial_number
        jdict['dfe-sn'] = dfe_serial_number
        jdict['result'] = result
        jdict['subjects'] = subjects
        jdict['afe'] = afe

        super().__init__(tag, None, rec, jdict)
