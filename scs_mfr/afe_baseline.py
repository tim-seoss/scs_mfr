#!/usr/bin/env python3

"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

calibration workflow:
    1: ./rtc.py -i -s -v
    2: ./pt1000_calib.py -s -v
    3: ./afe_calib -s AFE_SERIAL_NUMBER
  > 4: ./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET

Creates AFEBaseline document.

command line example:
./afe_baseline.py -v -1 -22
"""

import datetime
import sys

from scs_core.data.json import JSONify
from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.sensor_baseline import SensorBaseline

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_afe_baseline import CmdAFEBaseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAFEBaseline()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


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
