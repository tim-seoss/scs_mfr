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


# --------------------------------------------------------------------------------------------------------------------

v20 = 0.295         # a "representative" v20 - we need this to kick the process off


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.open(Host.I2C_SENSORS)


        # ------------------------------------------------------------------------------------------------------------
        # resource...

        sht_conf = SHTConf.load_from_host(Host)
        sht = sht_conf.int_sht()

        pt1000_calib = Pt1000Calib(None, v20)
        pt1000 = pt1000_calib.pt1000()

        afe = AFE(pt1000, [])


        # ------------------------------------------------------------------------------------------------------------
        # run...

        sht_datum = sht.sample()

        pt1000_datum = pt1000.sample(afe)

        v20 = pt1000_datum.v20(sht_datum.temp)

        pt1000_calib = Pt1000Calib(None, v20)
        pt1000_calib.save(Host)

        jstr = JSONify.dumps(pt1000_calib)
        print(jstr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        I2C.close()
