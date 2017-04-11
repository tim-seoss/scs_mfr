#!/usr/bin/env python3

"""
Created on 1 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.gas.afe import AFE
from scs_dfe.gas.pt1000_calib import Pt1000Calib

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_pt1000_calib import CmdPt1000Calib


# --------------------------------------------------------------------------------------------------------------------

v20 = 0.295         # a "representative" v20 - we need this to kick the process off


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.open(Host.I2C_SENSORS)

        # ----------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdPt1000Calib()

        if cmd.verbose:
            print(cmd, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        sht_conf = SHTConf.load_from_host(Host)
        sht = sht_conf.int_sht()

        pt1000_calib = Pt1000Calib(None, v20)
        pt1000 = pt1000_calib.pt1000()

        afe = AFE(pt1000, [])


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # SHT...
        sht_datum = sht.sample()

        if cmd.verbose:
            print(sht_datum, file=sys.stderr)

        # Pt1000 initial...
        pt1000_datum = afe.sample_temp()

        if cmd.set:
            # Pt1000 correction...
            v20 = pt1000_datum.v20(sht_datum.temp)

            pt1000_calib = Pt1000Calib(None, v20)
            pt1000_calib.save(Host)

            # Pt1000 final...
            if cmd.verbose:
                pt1000 = pt1000_calib.pt1000()
                afe = AFE(pt1000, [])

                pt1000_datum = afe.sample_temp()

                print(pt1000_datum, file=sys.stderr)

        # calibration...
        pt1000_calib = Pt1000Calib.load_from_host(Host)

        print(JSONify.dumps(pt1000_calib))


        if cmd.verbose:
            pt1000_calib = Pt1000Calib.load_from_host(Host)
            pt1000 = pt1000_calib.pt1000()

            afe = AFE(pt1000, [])

            print(pt1000.sample(afe), file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        I2C.close()
