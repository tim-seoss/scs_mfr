#!/usr/bin/env python3

"""
Created on 29 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_mfr/dfe_test.py 123 -g -v
"""

import os.path
import sys

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.location.gprmc import GPRMC
from scs_core.sys.eeprom_image import EEPROMImage

from scs_dfe.board.cat24c32 import CAT24C32
from scs_dfe.board.mcp9808 import MCP9808
from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.gas.afe import AFE
from scs_dfe.gas.afe_conf import AFEConf
from scs_dfe.gas.pt1000_calib import Pt1000Calib
from scs_dfe.gps.pam7q import PAM7Q
from scs_dfe.particulate.opc_n2 import OPCN2

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_dfe_test import CmdDFETest
from scs_mfr.report.dfe_test_datum import DFETestDatum
from scs_mfr.report.dfe_test_reporter import DFETestReporter


# TODO: add UUID read

# TODO: add int / ext sht

# --------------------------------------------------------------------------------------------------------------------
# validate...

if not os.path.isfile(Host.DFE_EEP_IMAGE):
    print("error: eeprom image not found", file=sys.stderr)
    exit()


# ----------------------------------------------------------------------------------------------------------------
# cmd...

cmd = CmdDFETest()

if not cmd.is_valid():
    cmd.print_help(sys.stderr)
    exit()


# --------------------------------------------------------------------------------------------------------------------
# config...

opc = None
afe_datum = None

reporter = DFETestReporter(cmd.verbose)

Host.enable_eeprom_access()


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.open(Host.I2C_SENSORS)

        # ------------------------------------------------------------------------------------------------------------
        # UUID...


        # ------------------------------------------------------------------------------------------------------------
        # Board temp...

        if cmd.verbose:
            print("Board temp...", file=sys.stderr)

        try:
            sensor = MCP9808(True)

            datum = sensor.sample()

            if cmd.verbose:
                print(datum, file=sys.stderr)

            temp = datum.temp

            ok = 10 < temp < 50
            reporter.report_test("BoardTemp", ok)

        except Exception as ex:
            reporter.report_exception("BoardTemp", ex)
            ok = False


        # ------------------------------------------------------------------------------------------------------------
        # OPC...

        if cmd.verbose:
            print("OPC...", file=sys.stderr)

        try:
            opc = OPCN2()
            opc.power_on()
            opc.operations_on()

            firmware = opc.firmware()

            if cmd.verbose:
                print(firmware, file=sys.stderr)

            ok = len(firmware) > 0
            reporter.report_test("OPC", ok)

        except Exception as ex:
            reporter.report_exception("OPC", ex)
            ok = False

        finally:
            if opc:
                opc.operations_off()
                opc.power_off()


        # ------------------------------------------------------------------------------------------------------------
        # GPS...

        if cmd.ignore_gps:
            reporter.report_ignore("GPS")

        else:
            if cmd.verbose:
                print("GPS...", file=sys.stderr)

            gps = PAM7Q()

            try:
                gps.power_on()
                gps.open()

                msg = gps.report(GPRMC)

                if cmd.verbose:
                    print(msg, file=sys.stderr)

                ok = msg is not None
                reporter.report_test("GPS", ok)

            except Exception as ex:
                reporter.report_exception("GPS", ex)
                ok = False

            finally:
                if opc:
                    gps.close()
                    gps.power_off()


        # ------------------------------------------------------------------------------------------------------------
        # NDIR...


        # ------------------------------------------------------------------------------------------------------------
        # SHT...

        if cmd.verbose:
            print("SHT...", file=sys.stderr)

        try:
            sht_conf = SHTConf.load_from_host(Host)
            sht = sht_conf.ext_sht()

            sht.reset()
            datum = sht.sample()

            if cmd.verbose:
                print(datum, file=sys.stderr)

            humid = datum.humid
            temp = datum.temp

            ok = 10 < humid < 90 and 10 < temp < 50
            reporter.report_test("SHT", ok)

        except Exception as ex:
            reporter.report_exception("SHT", ex)
            ok = False


        # ------------------------------------------------------------------------------------------------------------
        # AFE...

        if cmd.verbose:
            print("AFE...", file=sys.stderr)

        try:
            calib = Pt1000Calib.load_from_host(Host)
            pt1000 = calib.pt1000()

            conf = AFEConf.load_from_host(Host)
            sensors = conf.sensors()

            afe = AFE(pt1000, sensors)
            afe_datum = afe.sample()

            if cmd.verbose:
                print(afe_datum, file=sys.stderr)

            ok = 0.4 < afe_datum.pt1000.v < 0.6

            for gas, sensor in afe_datum.sns.items():
                sensor_ok = 0.9 < sensor.weV < 1.1 and 0.9 < sensor.aeV < 1.1

                if not sensor_ok:
                    ok = False

            reporter.report_test("AFE", ok)

        except Exception as ex:
            reporter.report_exception("AFE", ex)
            ok = False

    except RuntimeError:
        pass

    finally:
        I2C.close()


    try:
        I2C.open(Host.I2C_EEPROM)

        # ------------------------------------------------------------------------------------------------------------
        # EEPROM...

        if cmd.ignore_eeprom:
            reporter.report_ignore("EEPROM")

        else:
            if cmd.verbose:
                print("EEPROM...", file=sys.stderr)

            try:
                eeprom = CAT24C32()

                file_image = EEPROMImage.construct_from_file(Host.DFE_EEP_IMAGE, CAT24C32.SIZE)
                eeprom.write(file_image)

                ok = eeprom.image == file_image
                reporter.report_test("EEPROM", ok)

            except Exception as ex:
                reporter.report_exception("EEPROM", ex)
                ok = False


        # ------------------------------------------------------------------------------------------------------------
        # end...

    except RuntimeError:
        pass

    finally:
        I2C.close()


    # ----------------------------------------------------------------------------------------------------------------
    # result...

    if cmd.verbose:
        print(reporter, file=sys.stderr)

    reporter.report_result()


    # ----------------------------------------------------------------------------------------------------------------
    # report...

    recorded = LocalizedDatetime.now()
    datum = DFETestDatum(recorded, cmd.serial_number, reporter.subjects, afe_datum)

    print(JSONify.dumps(datum))
