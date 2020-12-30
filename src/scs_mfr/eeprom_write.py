#!/usr/bin/env python3

"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The eeprom_read utility write the contents of the given file to a South Coast Science digital front-end (DFE) board's
EEPROM.

The EEPROM contains information on vendor, product ID and a universally unique ID (UUID) code, as specified by either
the Raspberry Pi HAT or BeagleBone cape standards.

A jumper link must be fitted to the DFE board in order to enable the write operation.

SYNOPSIS
eeprom_write.py [-v] FILENAME

EXAMPLES
./eeprom_write.py ~/SCS/hat.eep

SEE ALSO
scs_mfr/dfe_id
scs_mfr/eeprom_read

BUGS
Not currently functional on BeagleBone systems.

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

from os import path

import sys

from scs_core.sys.eeprom_image import EEPROMImage

from scs_dfe.interface.component.cat24c32 import CAT24C32

from scs_host.bus.i2c import I2C

from scs_mfr.cmd.cmd_eeprom_write import CmdEEPROMWrite


# --------------------------------------------------------------------------------------------------------------------

# Host.enable_eeprom_access()


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.EEPROM.open()


        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdEEPROMWrite()

        if cmd.verbose:
            print(cmd, file=sys.stderr)
            print("-")


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        eeprom = CAT24C32()

        if not cmd.is_valid():
            cmd.print_help(sys.stderr)
            exit(2)

        if not path.isfile(cmd.filename):
            print("eeprom_write: file not found", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("current eeprom image:")
            eeprom.image.formatted(32)
            print("-")


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # file image...
        file_image = EEPROMImage.construct_from_file(cmd.filename, CAT24C32.SIZE)

        if cmd.verbose:
            print("file image:")
            file_image.formatted(32)
            print("-")

        # write...
        eeprom.write(file_image)

        if cmd.verbose:
            print("eeprom:")
            eeprom.image.formatted(32)
            print("-")

        # verify...
        verified = eeprom.image == file_image

        if not verified:
            print("eeprom_write: verification failed", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("verified:%s" % verified)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    finally:
        I2C.EEPROM.close()
