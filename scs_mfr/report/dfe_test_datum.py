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

    def __init__(self, rec, serial_number, subjects, afe):
        """
        Constructor
        """
        super().__init__(rec, ('sn', serial_number), ('subjects', subjects), ('afe', afe))
