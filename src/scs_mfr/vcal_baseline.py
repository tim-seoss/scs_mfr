#!/usr/bin/env python3

"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The baseline utility is used to adjust the zero offset of the reported vCal value. A positive offset value
cause the output to be higher.

IMPORTANT NOTE: the vCal baseline does not change the vCal value as reported by the gases_sampler utility. Instead,
it is used by the gas exegesis system, as part of the preprocessing of data that is passed to the interpretation
model.

Each sensor is identified by the gas that it detects. For example, a nitrogen dioxide sensor is identified as NO2, and
an ozone sensor is identified as Ox.

Note that the greengrass processes must be restarted for changes to take effect.

SYNOPSIS
baseline.py [{ -b GAS  | { -s | -o } GAS VALUE  | -z | -d }] [-v]

EXAMPLES
./baseline.py -s NO2 16

DOCUMENT EXAMPLE
{"CO": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 2},
"NO2": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 16}}

FILES
~/SCS/conf/baseline.json

SEE ALSO
scs_dev/gases_sampler
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.gas.sensor_baseline import SensorBaseline

from scs_core.model.gas.vcal_baseline import VCalBaseline

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_vcal_baseline import CmdVCalBaseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    sht = None
    barometer = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdVCalBaseline()

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

        baseline = VCalBaseline.load(Host, skeleton=True)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        now = LocalizedDatetime.now().utc()

        # update...
        if cmd.update():
            old_offset = baseline.sensor_offset(cmd.gas_name())

            if cmd.set:
                new_offset = cmd.set_value()

            else:
                new_offset = old_offset + cmd.offset_value()

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

            baseline = VCalBaseline({gas_name: sensor_baseline})

        # zero...
        if cmd.zero:
            for gas in baseline.gases():
                baseline.set_sensor_baseline(gas, SensorBaseline(now, 0))

            baseline.save(Host)

        # delete...
        if cmd.delete:
            VCalBaseline.delete(Host)
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
