#!/usr/bin/env python3

"""
Created on 29 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The dfe_test utility is used to perform a quality control test on South Coast Science digital front-end (DFE) boards.
The test exercises the ADCs and connectors.

The output of the test is a JSON document, summarising the result of each of a series of tests.

Ideally, a standard resistor load should be attached to the AFE connector of the DFE before the test is run.

SYNOPSIS
dfe_test.py [-e] [-g] [-r] [-v] DFE_SERIAL_NUMBER

EXAMPLES
./dfe_test.py -g -r -v 123

DOCUMENT EXAMPLE - OUTPUT
{"tag": "scs-ap1-6", "rec": "2018-04-06T16:08:45.037+00:00",
"val": {"host-sn": "0000000040d4d158", "dfe-sn": "123", "result": "FAIL",
"subjects": {"RTC": "-", "BoardTemp": "OK", "OPC": "FAIL", "GPS": "-", "Int SHT": "OK", "Ext SHT": "OK",
"Pt1000": "OK", "AFE": "FAIL", "EEPROM": "OK"}, "afe": {"pt1": {"v": 0.323286, "tmp": 22.8},
"sns": {"CO": {"weV": 0.339005, "aeV": 0.257254, "weC": 0.042188, "cnc": 155.1},
"SO2": {"weV": 0.267942, "aeV": 0.275942, "weC": -0.009696, "cnc": -26.4},
"H2S": {"weV": 0.296192, "aeV": 0.285754, "weC": 0.026254, "cnc": 19.4},
"VOC": {"weV": 0.102627, "weC": 0.102037, "cnc": 1300.9}}}}}
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.sys.system_id import SystemID

from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_dfe_test import CmdDFETest

from scs_mfr.report.dfe_test_datum import DFETestDatum
from scs_mfr.report.dfe_test_reporter import DFETestReporter

from scs_mfr.test.afe_test import AFETest
from scs_mfr.test.eeprom_test import EEPROMTest
from scs_mfr.test.gps_test import GPSTest
from scs_mfr.test.opc_test import OPCTest
from scs_mfr.test.pt1000_test import Pt1000Test
from scs_mfr.test.rtc_test import RTCTest
from scs_mfr.test.sht_test import SHTTest


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdDFETest()

    if cmd.verbose:
        print("dfe_test: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SystemID...
    system_id = SystemID.load(Host)

    if system_id is None:
        print("dfe_test: SystemID not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print(system_id, file=sys.stderr)

    # Interface...
    conf = InterfaceConf.load(Host)
    interface = conf.interface()

    if cmd.verbose:
        print(interface, file=sys.stderr)
        sys.stderr.flush()

    reporter = DFETestReporter(cmd.verbose)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    afe_datum = None


    # ----------------------------------------------------------------------------------------------------------------
    # UUID...


    # ----------------------------------------------------------------------------------------------------------------
    # RTC...

    if cmd.ignore_rtc:
        reporter.report_ignore("RTC")

    else:
        try:
            test = RTCTest(interface, cmd.verbose)

            test_ok = test.conduct()
            reporter.report_test("RTC", test_ok)

        except Exception as ex:
            reporter.report_exception("RTC", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # OPC...

    try:
        test = OPCTest(interface, cmd.verbose)

        test_ok = test.conduct()
        reporter.report_test("OPC", test_ok)

    except Exception as ex:
        reporter.report_exception("OPC", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # GPS...

    if cmd.ignore_gps:
        reporter.report_ignore("GPS")

    else:
        try:
            test = GPSTest(interface, cmd.verbose)

            test_ok = test.conduct()
            reporter.report_test("GPS", test_ok)

        except Exception as ex:
            reporter.report_exception("GPS", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # NDIR...


    # ----------------------------------------------------------------------------------------------------------------
    # Int SHT...

    try:
        sht_conf = SHTConf.load(Host)
        sht = sht_conf.int_sht()

        test = SHTTest("Int SHT", sht, interface, cmd.verbose)

        test_ok = test.conduct()
        reporter.report_test("Int SHT", test_ok)

    except Exception as ex:
        reporter.report_exception("Int SHT", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # Ext SHT...

    try:
        sht_conf = SHTConf.load(Host)
        sht = sht_conf.ext_sht()

        test = SHTTest("Ext SHT", sht, interface, cmd.verbose)

        test_ok = test.conduct()
        reporter.report_test("Ext SHT", test_ok)

    except Exception as ex:
        reporter.report_exception("Ext SHT", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # Pt1000...

    try:
        test = Pt1000Test(interface, cmd.verbose)

        test_ok = test.conduct()
        reporter.report_test("Pt1000", test_ok)

    except Exception as ex:
        reporter.report_exception("Pt1000", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # AFE...

    try:
        test = AFETest(interface, cmd.verbose)

        test_ok = test.conduct()
        reporter.report_test("AFE", test_ok)

        afe_datum = test.datum

    except Exception as ex:
        reporter.report_exception("AFE", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # EEPROM...

    if cmd.ignore_eeprom:
        reporter.report_ignore("EEPROM")

    else:
        try:
            test = EEPROMTest(interface, cmd.verbose)

            test_ok = test.conduct()
            reporter.report_test("EEPROM", test_ok)

        except Exception as ex:
            reporter.report_exception("EEPROM", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # result...

    if cmd.verbose:
        print(reporter, file=sys.stderr)
        print(reporter.result, file=sys.stderr)
        print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # report...

    recorded = LocalizedDatetime.now().utc()
    datum = DFETestDatum(system_id.message_tag(), recorded, Host.serial_number(), cmd.dfe_serial_number,
                         reporter.subjects, afe_datum, reporter.result)

    print(JSONify.dumps(datum))
