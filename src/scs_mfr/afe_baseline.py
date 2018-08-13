#!/usr/bin/env python3

"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The afe_baseline utility is used to adjust the zero offset for electrochemical sensors. For example, if a sensor reports
a concentration of 25 parts per billion in zero air, its zero offset should be set to -25. The date / time
of any change is recorded.

Each sensor is identified by the gas that it detects. For example, a nitrogen dioxide sensor is identified as NO2, and
an ozone sensor is identified as Ox.

Note that the scs_dev/gasses_sampler process must be restarted for changes to take effect.

SYNOPSIS
afe_baseline.py { { -s | -u | -d } GAS VALUE | -z } [-v]

EXAMPLES
./afe_baseline.py -s CO -24

DOCUMENT EXAMPLE
{"sn1": {"calibrated-on": "2017-10-04T17:18:31.832+01:00", "offset": 0},
"sn2": {"calibrated-on": "2017-06-20T00:00:00.000+01:00", "offset": 0},
"sn3": {"calibrated-on": "2017-06-20T00:00:00.000+01:00", "offset": 0},
"sn4": {"calibrated-on": "2017-06-20T00:00:00.000+01:00", "offset": 0}}

FILES
~/SCS/conf/afe_baseline.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/afe_calib
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.sensor_baseline import SensorBaseline

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_afe_baseline import CmdAFEBaseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAFEBaseline()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("afe_baseline: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    afe_baseline = AFEBaseline.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    # update...
    if cmd.set or cmd.up or cmd.down:
        calib = AFECalib.load(Host)

        if calib is None:
            print("afe_baseline: no AFE calibration document available.", file=sys.stderr)
            exit(1)

        gas_name = cmd.gas_name()

        index = calib.sensor_index(gas_name)

        if index is None:
            print("afe_baseline: the gas type is not supported by this AFE calibration document.", file=sys.stderr)
            exit(1)

        if cmd.set:
            new_offset = cmd.offset_value()

        elif cmd.up:
            old_offset = afe_baseline.sensor_baseline(index).offset
            new_offset = old_offset + cmd.offset_value()

        else:
            old_offset = afe_baseline.sensor_baseline(index).offset
            new_offset = old_offset - cmd.offset_value()

        now = LocalizedDatetime.now()

        afe_baseline.set_sensor_baseline(index, SensorBaseline(now, new_offset))
        afe_baseline.save(Host)

    # zero...
    elif cmd.zero:
        now = LocalizedDatetime.now()

        for i in range(len(afe_baseline)):
            afe_baseline.set_sensor_baseline(i, SensorBaseline(now, 0))

        afe_baseline.save(Host)

    # report...
    print(JSONify.dumps(afe_baseline))
