#!/usr/bin/env python3

"""
Created on 29 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Raspberry Pi:
https://github.com/raspberrypi/hats/tree/master/eepromutils

https://www.raspberrypi.org/documentation/configuration/device-tree.md


BeagleBone:
http://azkeller.com/blog/?p=62

https://github.com/jbdatko/eeprom_tutorial/blob/master/eeprom.md
https://github.com/picoflamingo/BBCape_EEPROM

http://papermint-designs.com/community/node/331

https://learn.adafruit.com/introduction-to-the-beaglebone-black-device-tree/compiling-an-overlay


command line example:
./scs_mfr/eeprom_write.py -v /home/pi/SCS/hat.eep
"""

import os.path
import sys

from scs_core.sys.eeprom_image import EEPROMImage

from scs_dfe.board.cat24c32 import CAT24C32
from scs_dfe.bus.i2c import I2C
from scs_dfe.board.mcp9808 import MCP9808
from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.gas.afe import AFE
from scs_dfe.gas.afe_conf import AFEConf
from scs_dfe.gas.pt1000_calib import Pt1000Calib
from scs_dfe.particulate.opc_n2 import OPCN2

from scs_host.sys.host import Host

from scs_mfr.report.dfe_test_reporter import TestReporter


# --------------------------------------------------------------------------------------------------------------------
# config...

eeprom_image_name = '/home/pi/SCS/hat.eep'           # hard-coded path
opc = None

reporter = TestReporter()


# --------------------------------------------------------------------------------------------------------------------

# validate...

if not os.path.isfile(eeprom_image_name):
    print("error: eeprom image not found", file=sys.stderr)
    exit()


# --------------------------------------------------------------------------------------------------------------------

Host.enable_eeprom_access()


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.open(Host.I2C_EEPROM)


        # ------------------------------------------------------------------------------------------------------------
        # EEPROM...

        print("EEPROM...", file=sys.stderr)

        # write...
        try:
            eeprom = CAT24C32()

            file_image = EEPROMImage.construct_from_file(eeprom_image_name, CAT24C32.SIZE)
            eeprom.write(file_image)

            ok = eeprom.image == file_image

        except Exception as ex:
            reporter.report_exception(ex, True)
            ok = False

        # report...
        reporter.report_test(ok)

    except RuntimeError:
        pass

    finally:
        I2C.close()

    try:
        I2C.open(Host.I2C_SENSORS)

        # ------------------------------------------------------------------------------------------------------------
        # Board temp...

        print("Board temp...", file=sys.stderr)

        try:
            sensor = MCP9808(True)

            datum = sensor.sample()
            print(datum, file=sys.stderr)

            temp = datum.temp
            ok = 10 < temp < 50

        except Exception as ex:
            reporter.report_exception(ex, False)
            ok = False

        # report...
        reporter.report_test(ok)


        # ------------------------------------------------------------------------------------------------------------
        # OPC...

        print("OPC...", file=sys.stderr)

        try:
            sensor = OPCN2()
            sensor.on()

            firmware = sensor.firmware()
            print(firmware, file=sys.stderr)

            ok = len(firmware) > 0

        except Exception as ex:
            reporter.report_exception(ex, False)
            ok = False

        finally:
            if sensor:
                sensor.off()

        # report...
        reporter.report_test(ok)


        # ------------------------------------------------------------------------------------------------------------
        # NDIR...


        # ------------------------------------------------------------------------------------------------------------
        # SHT...

        print("SHT...", file=sys.stderr)

        try:
            sht_conf = SHTConf.load(Host)
            sht = sht_conf.ext_sht()

            sht.reset()

            datum = sht.sample()
            print(datum, file=sys.stderr)

            humid = datum.humid
            temp = datum.temp

            ok = 10 < humid < 90 and 10 < temp < 50

        except Exception as ex:
            reporter.report_exception(ex, False)
            ok = False

        # report...
        reporter.report_test(ok)


        # ------------------------------------------------------------------------------------------------------------
        # AFE...

        try:
            calib = Pt1000Calib.load(Host)
            pt1000 = calib.pt1000()

            conf = AFEConf.load(Host)
            sensors = conf.sensors()

            afe = AFE(pt1000, sensors)
            datum = afe.sample()

            print(datum, file=sys.stderr)

            ok = 0.4 < datum.pt1000.v < 0.6

            for gas, sensor in datum.sns.items():
                sensor_ok = 0.9 < sensor.weV < 1.1 and 0.9 < sensor.aeV < 1.1

                if not sensor_ok:
                    ok = False

        except Exception as ex:
            reporter.report_exception(ex, False)
            ok = False
            raise ex

        # report...
        reporter.report_test(ok)


        # ------------------------------------------------------------------------------------------------------------
        # result...

        reporter.report_result()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    # except Exception as ex:
    #     pass

    finally:
        I2C.close()
