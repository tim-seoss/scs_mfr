#!/usr/bin/env python3

"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Creates AFECalib document.

command line example:
./afe_calib.py -v -s 15-000064
"""

import datetime
import sys

from scs_core.data.json import JSONify

from scs_dfe.gas.afe_baseline import AFEBaseline
from scs_dfe.gas.sensor_baseline import SensorBaseline

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_afe_baseline import CmdAFEBaseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAFEBaseline()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    now = datetime.datetime.now()

    baseline = AFEBaseline.load_from_host(Host)

    if cmd.set():
        for i, offset in cmd.offsets.items():
            if offset is not None:
                baseline.set_sensor_baseline(i, SensorBaseline(now.date(), offset))

        baseline.save(Host)

    print(JSONify.dumps(baseline))
