#!/usr/bin/env python3

# noinspection PyUnboundLocalVariable
"""
Created on 29 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./dfe_test.py 123 -g -v
"""

import os.path
import sys

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sys.eeprom_image import EEPROMImage
from scs_core.sys.system_id import SystemID

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.pt1000_calib import Pt1000Calib

from scs_dfe.board.cat24c32 import CAT24C32

from scs_dfe.climate.sht_conf import SHTConf

from scs_dfe.gas.afe import AFE
from scs_dfe.gas.pt1000 import Pt1000

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_dfe_test import CmdDFETest
from scs_mfr.report.dfe_test_datum import DFETestDatum
from scs_mfr.report.dfe_test_reporter import DFETestReporter

from scs_mfr.test.board_temp_test import BoardTempTest
from scs_mfr.test.gps_test import GPSTest
from scs_mfr.test.opc_test import OPCTest
from scs_mfr.test.rtc_test import RTCTest
from scs_mfr.test.sht_test import SHTTest


# TODO: remove Pt1000 calibration
# TODO: add result to output
# TODO: add UUID read

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

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SystemID...
    system_id = SystemID.load_from_host(Host)

    if system_id is None:
        print("SystemID not available.", file=sys.stderr)
        exit()

    if cmd.verbose:
        print(system_id, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    dfe_ok = True

    try:
        I2C.open(Host.I2C_SENSORS)

        # ------------------------------------------------------------------------------------------------------------
        # UUID...


        # ------------------------------------------------------------------------------------------------------------
        # RTC...

        try:
            test_ok = RTCTest.conduct(cmd.verbose)
            reporter.report_test("RTC", test_ok)

        except Exception as ex:
            reporter.report_exception("RTC", ex)
            test_ok = False

        if not test_ok:
            dfe_ok = False


        # ------------------------------------------------------------------------------------------------------------
        # Board temp...

        try:
            test_ok = BoardTempTest.conduct(cmd.verbose)
            reporter.report_test("BoardTemp", test_ok)

        except Exception as ex:
            reporter.report_exception("BoardTemp", ex)
            test_ok = False

        if not test_ok:
            dfe_ok = False


        # ------------------------------------------------------------------------------------------------------------
        # OPC...

        try:
            test_ok = OPCTest.conduct(cmd.verbose)
            reporter.report_test("OPC", test_ok)

        except Exception as ex:
            reporter.report_exception("OPC", ex)
            test_ok = False

        if not test_ok:
            dfe_ok = False


        # ------------------------------------------------------------------------------------------------------------
        # GPS...

        if cmd.ignore_gps:
            reporter.report_ignore("GPS")

        else:
            try:
                test_ok = GPSTest.conduct(cmd.verbose)
                reporter.report_test("GPS", test_ok)

            except Exception as ex:
                reporter.report_exception("GPS", ex)
                test_ok = False

            if not test_ok:
                dfe_ok = False


        # ------------------------------------------------------------------------------------------------------------
        # NDIR...


        # ------------------------------------------------------------------------------------------------------------
        # Ext SHT...

        try:
            sht_conf = SHTConf.load_from_host(Host)
            sht = sht_conf.ext_sht()

            test_ok = SHTTest.conduct("Ext SHT", sht, cmd.verbose)
            reporter.report_test("Ext SHT", test_ok)

        except Exception as ex:
            reporter.report_exception("Ext SHT", ex)
            test_ok = False

        if not test_ok:
            dfe_ok = False


        # ------------------------------------------------------------------------------------------------------------
        # Int SHT...

        try:
            sht_conf = SHTConf.load_from_host(Host)
            sht = sht_conf.int_sht()

            test_ok = SHTTest.conduct("Int SHT", sht, cmd.verbose)
            reporter.report_test("Int SHT", test_ok)

        except Exception as ex:
            reporter.report_exception("Int SHT", ex)
            test_ok = False

        if not test_ok:
            dfe_ok = False


        # ------------------------------------------------------------------------------------------------------------
        # Pt1000 calibration...

        if cmd.verbose:
            print("Pt1000...", file=sys.stderr)
            print("(calibrating with Int SHT)", file=sys.stderr)

        pt1000 = None

        try:
            # resources...
            calib = Pt1000Calib.load_from_host(Host)
            pt1000 = Pt1000(calib)

            afe = AFE(pt1000, [])

            # initial sample...
            pt1000_datum = afe.sample_temp()

            v20 = pt1000_datum.v20(int_sht_datum.temp)

            # calibrate...
            calib = Pt1000Calib(None, v20)
            calib.save(Host)

            # new resource...
            pt1000 = Pt1000(calib)

            afe = AFE(pt1000, [])

            # final sample...
            pt1000_datum = afe.sample_temp()

            if cmd.verbose:
                print(pt1000_datum, file=sys.stderr)

            temp_diff = abs(pt1000_datum.temp - int_sht_datum.temp)

            ok = temp_diff < 0.2
            reporter.report_test("Pt1000", ok)

        except Exception as ex:
            reporter.report_exception("Pt1000", ex)
            ok = False


        # ------------------------------------------------------------------------------------------------------------
        # AFE...

        if cmd.verbose:
            print("AFE...", file=sys.stderr)

        try:
            afe_baseline = AFEBaseline.load_from_host(Host)

            calib = AFECalib.load_from_host(Host)
            sensors = calib.sensors(afe_baseline)

            afe = AFE(pt1000, sensors)
            afe_datum = afe.sample()

            if cmd.verbose:
                print(afe_datum, file=sys.stderr)

            # noinspection PyTypeChecker
            ok = 0.4 < afe_datum.pt1000.v < 0.6

            for gas, sensor in afe_datum.sns.items():
                # noinspection PyTypeChecker
                sensor_ok = 0.9 < sensor.we_v < 1.1 and 0.9 < sensor.ae_v < 1.1

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
    datum = DFETestDatum(system_id.message_tag(), recorded, Host.serial_number(), cmd.dfe_serial_number,
                         reporter.subjects, afe_datum)

    print(JSONify.dumps(datum))
