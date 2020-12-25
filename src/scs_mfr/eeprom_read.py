#!/usr/bin/env python3

"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The eeprom_read utility presents a formatted copy of the South Coast Science digital front-end (DFE) board's EEPROM
contents to stdout.

The EEPROM contains information on vendor, product ID and a universally unique ID (UUID) code, as specified by either
the Raspberry Pi HAT or BeagleBone cape standards.

SYNOPSIS
eeprom_read.py

EXAMPLES
./eeprom_read.py

SEE ALSO
scs_mfr/dfe_id
scs_mfr/eeprom_write

RESOURCES
https://github.com/raspberrypi/hats
https://github.com/picoflamingo/BBCape_EEPROM

https://lb.raspberrypi.org/forums/viewtopic.php?t=108134

https://github.com/raspberrypi/hats/tree/master/eepromutils
https://www.raspberrypi.org/documentation/configuration/device-tree.md

https://github.com/jbdatko/eeprom_tutorial
http://azkeller.com/blog/?p=62
http://papermint-designs.com/community/node/331
https://learn.adafruit.com/introduction-to-the-beaglebone-black-device-tree/compiling-an-overlay
"""

from scs_dfe.interface.component.cat24c32 import CAT24C32

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

Host.enable_eeprom_access()


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.EEPROM.open()


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        eeprom = CAT24C32()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        eeprom.image.formatted(32)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    finally:
        I2C.EEPROM.close()
