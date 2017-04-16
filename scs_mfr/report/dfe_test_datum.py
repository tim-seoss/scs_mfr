"""
Created on 29 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sample.sample_datum import SampleDatum


# TODO: add an AFETestDatum class to reduce the amount of rubbish

# --------------------------------------------------------------------------------------------------------------------

class DFETestDatum(SampleDatum):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, host_serial_number, dfe_serial_number, subjects, afe):
        """
        Constructor
        """
        super().__init__(tag, rec, ('host_sn', host_serial_number), ('dfe_sn', dfe_serial_number),
                         ('subjects', subjects), ('afe', afe))
