#!/usr/bin/env python3

"""
Created on 2 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The scd30_baseline utility is used to adjust the zero offset for the Sensirion SCD30 NDIR CO2 sensor.

If the system reports a concentration of 25 parts per billion in zero air, its zero offset should be set to -25.
The date / time of any change is recorded.

Note that the scs_dev/gasses_sampler process must be restarted for changes to take effect.

SYNOPSIS
scd30_baseline.py [{ { { -s | -o } VALUE | -c CORRECT REPORTED } [-t TEMP -m HUMID [-p PRESS]] | -z }] [-v]

EXAMPLES
./scd30_baseline.py -c 10 23

DOCUMENT EXAMPLE
{"baseline": {"calibrated-on": "2019-02-02T11:34:16Z", "offset": 50}}

FILES
~/SCS/conf/scd30_baseline.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/scd30_conf
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.gas.scd30.scd30_baseline import SCD30Baseline
from scs_core.gas.sensor_baseline import SensorBaseline, SensorBaselineSample

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_scd30_baseline import CmdSCD30Baseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    sht = None
    barometer = None

    now = LocalizedDatetime.now().utc()

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSCD30Baseline()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("scd30_baseline: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        I2C.Sensors.open()

        # ------------------------------------------------------------------------------------------------------------
        # resources...

        scd30_baseline = SCD30Baseline.load(Host, skeleton=True)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # sample...
        sample = SensorBaselineSample(None, cmd.humid, cmd.temp, cmd.press) if cmd.has_sample() \
            else None

        # update...
        if cmd.update():
            old_offset = scd30_baseline.sensor_baseline.offset

            if cmd.set_value:
                new_offset = cmd.set_value

            elif cmd.offset_value:
                new_offset = old_offset + cmd.offset_value

            else:
                old_offset = scd30_baseline.sensor_baseline.offset
                new_offset = old_offset + (cmd.correct_value - cmd.reported_value)

            scd30_baseline = SCD30Baseline(SensorBaseline(now, new_offset, sample=sample))
            scd30_baseline.save(Host)

            if cmd.verbose:
                print("scd30_baseline: was: %s now: %s" % (old_offset, new_offset), file=sys.stderr)

        # zero...
        elif cmd.zero:
            scd30_baseline = SCD30Baseline(SensorBaseline(now, 0))
            scd30_baseline.save(Host)

        # report...
        print(JSONify.dumps(scd30_baseline, indent=cmd.indent))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("scd30_baseline: KeyboardInterrupt", file=sys.stderr)

    finally:
        I2C.Sensors.close()
