#!/usr/bin/env python3

"""
Created on 2 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The scd30_baseline utility is used to adjust the zero offset for the Sensirion SCD30 NDIR CO2 sensor.

If the system reports a concentration of 25 parts per billion in zero air, its zero offset should be set to -25.
The date / time of any change is recorded.

The environmental temperature, relative humidity and, optionally, absolute barometric pressure are stored alongside
the offset. These environmental parameters may be sourced either from sensors at the moment at which the offset is
recorded (the default), or supplied on the command line.

Note that the scs_dev/gasses_sampler process must be restarted for changes to take effect.

SYNOPSIS
scd30_baseline.py [{ { { -s | -o } VALUE | -c CORRECT REPORTED } [-r HUMID -t TEMP [-p PRESS]] | -z }] [-v]

EXAMPLES
./scd30_baseline.py -c 10 23

DOCUMENT EXAMPLE
{"baseline": {"calibrated-on": "2019-02-02T11:34:16Z", "offset": 50, "env": {"hmd": 66.0, "tmp": 11.0, "pA": 99.0}}}

FILES
~/SCS/conf/scd30_baseline.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/scd30_conf
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.climate.mpl115a2_conf import MPL115A2Conf

from scs_core.gas.scd30.scd30_baseline import SCD30Baseline
from scs_core.gas.sensor_baseline import SensorBaseline, BaselineEnvironment

from scs_dfe.climate.mpl115a2 import MPL115A2
from scs_dfe.climate.sht_conf import SHTConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_scd30_baseline import CmdSCD30Baseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    sht = None
    mpl = None

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

        scd30_baseline = SCD30Baseline.load(Host)

        if not cmd.env_is_specified():
            # SHTConf...
            sht_conf = SHTConf.load(Host)

            if sht_conf is None:
                print("scd30_baseline: SHTConf not available.", file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print("scd30_baseline: %s" % sht_conf, file=sys.stderr)

            # SHT...
            sht = sht_conf.int_sht()

            # MPL115A2Conf...
            mpl_conf = MPL115A2Conf.load(Host)

            if mpl_conf is not None:
                if cmd.verbose:
                    print("scd30_baseline: %s" % mpl_conf, file=sys.stderr)

                # MPL115A2...
                mpl = MPL115A2.construct(None)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if mpl is not None:
            mpl.init()

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

            if cmd.env_is_specified():
                humid = cmd.humid
                temp = cmd.temp
                press = cmd.press

            else:
                sht_datum = sht.sample()
                mpl_datum = None if mpl is None else mpl.sample()

                humid = sht_datum.humid
                temp = sht_datum.temp
                press = None if mpl_datum is None else mpl_datum.actual_press

            env = BaselineEnvironment(humid, temp, press)

            scd30_baseline = SCD30Baseline(SensorBaseline(now, new_offset, env))
            scd30_baseline.save(Host)

            if cmd.verbose:
                print("scd30_baseline: was: %s now: %s" % (old_offset, new_offset), file=sys.stderr)

        # zero...
        elif cmd.zero:
            scd30_baseline = SCD30Baseline(SensorBaseline(now, 0, None))
            scd30_baseline.save(Host)

        # report...
        print(JSONify.dumps(scd30_baseline))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("scd30_baseline: KeyboardInterrupt", file=sys.stderr)

    finally:
        I2C.Sensors.close()
