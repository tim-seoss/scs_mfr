#!/usr/bin/env python3

"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The afe_baseline utility is used to adjust the zero offset for electrochemical sensors. The offset can be positive or
negative, and represents a parts-per-billion value. Sensors are identified by their position on the Alphasense analogue
front-end (AFE) board: SN1 to SN4 (the PID station is referred to as SN4). The date / time of any change is recorded.

Note that the scs_dev/gasses_sampler process must be restarted for changes to take effect.

SYNOPSIS
afe_baseline.py [-1 SN1_OFFSET] [-2 SN2_OFFSET] [-3 SN3_OFFSET] [-4 SN3_OFFSET] [-v]

EXAMPLES
./afe_baseline.py -1 15

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
    # resources...

    baseline = AFEBaseline.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        now = LocalizedDatetime.now()

        for i, offset in cmd.offsets.items():
            if offset is not None:
                baseline.set_sensor_baseline(i, SensorBaseline(now, offset))

        baseline.save(Host)

    print(JSONify.dumps(baseline))
