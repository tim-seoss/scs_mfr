#!/usr/bin/env python3

"""
Created on 2 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The baseline utility is used to adjust the zero offset for the Sensirion SCD30 NDIR CO2 sensor.

If the system reports a concentration of 25 parts per billion in zero air, its zero offset should be set to -25.
The date / time of any change is recorded.

Note that the scs_dev/gasses_sampler process must be restarted for changes to take effect.

SYNOPSIS
scd30_baseline.py [{ { { -s | -o } VALUE | -c CORRECT REPORTED } [-t TEMP -m HUMID [-p PRESS]] | -z  | -d }] [-v]

EXAMPLES
./baseline.py -c 10 23

DOCUMENT EXAMPLE
{"CO2": {"calibrated-on": "2022-03-21T12:46:52Z", "offset": 321, "env": {"hmd": 54.3, "tmp": 21.3, "pA": 99.6}}}

FILES
~/SCS/conf/baseline.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/scd30_conf
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.gas.scd30.scd30_baseline import SCD30Baseline
from scs_core.gas.sensor_baseline import SensorBaseline, SensorBaselineSample

from scs_core.sys.logging import Logging

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

    Logging.config('scd30_baseline', verbose=cmd.verbose)
    logger = Logging.getLogger()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    logger.info(cmd)

    try:
        I2C.Sensors.open()

        # ------------------------------------------------------------------------------------------------------------
        # resources...

        baseline = SCD30Baseline.load(Host)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # sample...
        sample = SensorBaselineSample(None, cmd.humid, cmd.temp, cmd.press) if cmd.has_sample() \
            else None

        # update...
        if cmd.update():
            baseline = SCD30Baseline.load(Host, skeleton=True)

            old_offset = baseline.sensor_baseline.offset

            if cmd.set_value is not None:
                new_offset = cmd.set_value

            elif cmd.offset_value is not None:
                new_offset = old_offset + cmd.offset_value

            else:
                old_offset = baseline.sensor_baseline.offset
                new_offset = old_offset + (cmd.correct_value - cmd.reported_value)

            baseline = SCD30Baseline(SensorBaseline(now, new_offset, sample=sample))
            print("baseline: %s" % baseline)
            baseline.save(Host)

            logger.info("was: %s now: %s" % (old_offset, new_offset))

        # zero...
        elif cmd.zero:
            baseline = SCD30Baseline(SensorBaseline(now, 0))
            baseline.save(Host)

        # delete...
        if cmd.delete:
            SCD30Baseline.delete(Host)
            baseline = None

        # report...
        if baseline:
            print(JSONify.dumps(baseline, indent=cmd.indent))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        print(file=sys.stderr)

    finally:
        I2C.Sensors.close()
