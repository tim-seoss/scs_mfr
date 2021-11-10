#!/usr/bin/env python3

"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The afe_baseline utility is used to adjust the zero offset for electrochemical sensors, as interpreted by the
Alphasense application note AAN 803-02.

A positive offset value cause the result to be higher - if the system reports a concentration of 25 parts per billion
in zero air, its zero offset should be set to -25. The date / time of any change is recorded.

Each sensor is identified by the gas that it detects. For example, a nitrogen dioxide sensor is identified as NO2, and
an ozone sensor is identified as Ox.

Note that the scs_dev/gasses_sampler process must be restarted for changes to take effect.

SYNOPSIS
afe_baseline.py [{ -b GAS  | { -s | -o } GAS VALUE | -c GAS CORRECT REPORTED | -z }] [-v]

EXAMPLES
./afe_baseline.py -c NO2 10 23

DOCUMENT EXAMPLE
{"sn1": {"calibrated-on": "2019-02-02T12:00:48Z", "offset": 123},
"sn2": {"calibrated-on": "2019-02-02T11:30:17Z", "offset": 0},
"sn3": {"calibrated-on": "2019-02-02T11:30:17Z", "offset": 0},
"sn4": {"calibrated-on": "2019-02-02T11:30:17Z", "offset": 0}}

FILES
~/SCS/conf/afe_baseline.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/afe_calib
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify


from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib

from scs_core.gas.sensor_baseline import SensorBaseline

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_baseline import CmdBaseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    sht = None
    barometer = None

    now = LocalizedDatetime.now().utc()

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdBaseline()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("afe_baseline: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        I2C.Sensors.open()

        # ------------------------------------------------------------------------------------------------------------
        # resources...

        afe_baseline = AFEBaseline.load(Host, skeleton=True)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # update...
        if cmd.update():
            calib = AFECalib.load(Host)

            if calib is None:
                print("afe_baseline: no AFE calibration document available.", file=sys.stderr)
                exit(1)

            gas_name = cmd.gas_name()

            index = calib.sensor_index(gas_name)

            if index is None:
                print("afe_baseline: %s is not included in the AFE calibration document." % gas_name, file=sys.stderr)
                exit(1)

            old_offset = afe_baseline.sensor_baseline(index).offset

            if cmd.set:
                new_offset = cmd.set_value()

            elif cmd.offset:
                new_offset = old_offset + cmd.offset_value()

            else:
                old_offset = afe_baseline.sensor_baseline(index).offset
                new_offset = old_offset + (cmd.correct_value() - cmd.reported_value())

            afe_baseline.set_sensor_baseline(index, SensorBaseline(now, new_offset))
            afe_baseline.save(Host)

            if cmd.verbose:
                print("afe_baseline: %s: was: %s now: %s" % (cmd.gas_name(), old_offset, new_offset), file=sys.stderr)

        # baseline...
        elif cmd.baseline:
            calib = AFECalib.load(Host)

            gas_name = cmd.gas_name()
            index = calib.sensor_index(gas_name)

            if index is None:
                print("afe_baseline: %s is not included in the AFE calibration document." % gas_name, file=sys.stderr)
                exit(1)

            afe_baseline = AFEBaseline([afe_baseline.sensor_baseline(index)])

        # zero...
        elif cmd.zero:
            for index in range(len(afe_baseline)):
                afe_baseline.set_sensor_baseline(index, SensorBaseline(now, 0))

            afe_baseline.save(Host)

        # report...
        print(JSONify.dumps(afe_baseline))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("afe_baseline: KeyboardInterrupt", file=sys.stderr)

    finally:
        I2C.Sensors.close()
