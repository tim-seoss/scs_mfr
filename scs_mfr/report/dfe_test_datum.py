"""
Created on 29 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sample.sample_datum import SampleDatum


# --------------------------------------------------------------------------------------------------------------------

class DFETestDatum(SampleDatum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, host_serial_number, dfe_serial_number, subjects, afe, result):
        """
        Constructor
        """
        super().__init__(tag, rec, ('host-sn', host_serial_number), ('dfe-sn', dfe_serial_number),
                         ('subjects', subjects), ('afe', afe), ('result', result))
