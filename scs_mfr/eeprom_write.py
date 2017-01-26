#!/usr/bin/env python3

"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Raspberry Pi:
https://github.com/raspberrypi/hats/tree/master/eepromutils

BeagleBone:


command line example:
./scs_manufacture/eeprom_write.py /home/pi/hats/eepromutils/myhat.eep
"""

import os.path
import subprocess
import sys

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_dfe.board.cat24c32 import CAT24C32
from scs_dfe.board.eeprom_image import EEPROMImage
from scs_dfe.bus.i2c import I2C

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_eeprom_write import CmdEEPROMWrite


# --------------------------------------------------------------------------------------------------------------------

# Enable I2C bus 1 for EEPROM operations on RPi...
subprocess.call(['sudo', 'dtoverlay', 'i2c-gpio', 'i2c_gpio_sda=0', 'i2c_gpio_scl=1'])


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.open(Host.I2C_EEPROM)


        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdEEPROMWrite()

        if cmd.verbose:
            print(cmd, file=sys.stderr)
            print("-")


        # ------------------------------------------------------------------------------------------------------------
        # resource...

        eeprom = CAT24C32()

        if not cmd.is_valid():
            cmd.print_help(sys.stderr)
            I2C.close()
            exit()

        if not os.path.isfile(cmd.filename):
            print("error: file not found", file=sys.stderr)
            I2C.close()
            exit()

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
            print("error: verification failed", file=sys.stderr)
            I2C.close()
            exit()

        if cmd.verbose:
            print("verified:%s" % verified)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        I2C.close()
