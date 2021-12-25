#!/usr/bin/env python3

"""
Created on 19 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The baseline utility is used to adjust the zero offset for electrochemical sensors, as interpreted by the
current gas interpretation machine learning model.

WARNING: because ML models typically do not report negative values, the effect of raising the offset above zero is to
raise the limit of detection of the sensor system.

Each sensor is identified by the gas that it detects. For example, a nitrogen dioxide sensor is identified as NO2, and
an ozone sensor is identified as Ox.

Note that the scs_dev/gasses_sampler and greengrass processes must be restarted for changes to take effect.

WARNING:

SYNOPSIS
baseline.py [{ -b GAS  | { -s | -o } GAS VALUE | -c GAS CORRECT REPORTED | -z | -d }] [-v]

EXAMPLES
./baseline.py -c NO2 10 23

DOCUMENT EXAMPLE
{"CO": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 2},
"NO2": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 1}}

FILES
~/SCS/conf/baseline.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/afe_calib
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.gas.sensor_baseline import SensorBaseline

from scs_core.model.gas.gas_baseline import GasBaseline

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_baseline import CmdBaseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    sht = None
    barometer = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdBaseline()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("baseline: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    try:
        I2C.Sensors.open()

        # ------------------------------------------------------------------------------------------------------------
        # resources...

        baseline = GasBaseline.load(Host, skeleton=True)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        now = LocalizedDatetime.now().utc()

        # update...
        if cmd.update():
            old_offset = baseline.sensor_offset(cmd.gas_name())

            if cmd.set:
                new_offset = cmd.set_value()

            elif cmd.offset:
                new_offset = old_offset + cmd.offset_value()

            else:
                new_offset = old_offset + (cmd.correct_value() - cmd.reported_value())

            baseline.set_sensor_baseline(cmd.gas_name(), SensorBaseline(now, new_offset))
            baseline.save(Host)

            if cmd.verbose:
                print("baseline: %s: was: %s now: %s" % (cmd.gas_name(), old_offset, new_offset), file=sys.stderr)

        # baseline...
        if cmd.baseline:
            gas_name = cmd.gas_name()
            sensor_baseline = baseline.sensor_baseline(gas_name)

            if sensor_baseline is None:
                print("baseline: %s is not included in the calibration document." % gas_name, file=sys.stderr)
                exit(1)

            baseline = GasBaseline({gas_name: sensor_baseline})

        # zero...
        if cmd.zero:
            for gas in baseline.gases():
                baseline.set_sensor_baseline(gas, SensorBaseline(now, 0))

            baseline.save(Host)

        # delete...
        if cmd.delete:
            GasBaseline.delete(Host)
            baseline = None

        # report...
        if baseline:
            print(JSONify.dumps(baseline))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        pass

    finally:
        I2C.Sensors.close()
