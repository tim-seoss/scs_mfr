"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note that this test updates the EEPROM contents.
"""

from os import path

import sys

from scs_core.sys.eeprom_image import EEPROMImage

from scs_dfe.interface.component.cat24c32 import CAT24C32

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class EEPROMTest(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface, verbose):
        super().__init__(interface, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("EEPROM...", file=sys.stderr)

        # validate...
        if not path.isfile(Host.eep_image()):
            print("error: eeprom image not found", file=sys.stderr)
            exit(1)

        try:
            # resources...
            # Host.enable_eeprom_access()               # TODO: test whether EEPROM access is required

            I2C.EEPROM.open()

            eeprom = CAT24C32()

            # test...
            file_image = EEPROMImage.construct_from_file(Host.eep_image(), CAT24C32.SIZE)
            eeprom.write(file_image)

            # test criterion...
            return eeprom.image == file_image

        finally:
            I2C.EEPROM.close()
