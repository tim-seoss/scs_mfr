#!/usr/bin/env python3

"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The baseline utility is used to adjust the zero offset for electrochemical sensors, as interpreted by the
Alphasense application note AAN 803-02.

A positive offset value cause the result to be higher - if the system reports a concentration of 25 parts per billion
in zero air, its zero offset should be set to -25. The date / time of any change is recorded.

Each sensor is identified by the gas that it detects. For example, a nitrogen dioxide sensor is identified as NO2, and
an ozone sensor is identified as Ox.

Note that the scs_dev/gasses_sampler process must be restarted for changes to take effect.

SYNOPSIS
baseline.py [{ -b GAS  | { -s | -o } GAS VALUE | -c GAS CORRECT REPORTED | -z | -d }] [-v]

EXAMPLES
./baseline.py -c NO2 10 23

DOCUMENT EXAMPLE
{"sn1": {"calibrated-on": "2019-02-02T12:00:48Z", "offset": 123},
"sn2": {"calibrated-on": "2019-02-02T11:30:17Z", "offset": 0},
"sn3": {"calibrated-on": "2019-02-02T11:30:17Z", "offset": 0},
"sn4": {"calibrated-on": "2019-02-02T11:30:17Z", "offset": 0}}

FILES
~/SCS/conf/baseline.json

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

from scs_core.sys.logging import Logging

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

    Logging.config('afe_baseline', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    try:
        I2C.Sensors.open()

        # ------------------------------------------------------------------------------------------------------------
        # resources...

        baseline = AFEBaseline.load(Host, skeleton=True)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # update...
        if cmd.update():
            calib = AFECalib.load(Host)

            if calib is None:
                logger.error("no AFE calibration document available.")
                exit(1)

            gas_name = cmd.gas_name()

            index = calib.sensor_index(gas_name)

            if index is None:
                logger.error("%s is not included in the AFE calibration document." % gas_name)
                exit(1)

            old_offset = baseline.sensor_baseline(index).offset

            if cmd.set:
                new_offset = cmd.set_value()

            elif cmd.offset:
                new_offset = old_offset + cmd.offset_value()

            else:
                old_offset = baseline.sensor_baseline(index).offset
                new_offset = old_offset + (cmd.correct_value() - cmd.reported_value())

            baseline.set_sensor_baseline(index, SensorBaseline(now, new_offset))
            baseline.save(Host)

            logger.info("%s: was: %s now: %s" % (cmd.gas_name(), old_offset, new_offset))

        # baseline...
        if cmd.baseline:
            calib = AFECalib.load(Host)

            gas_name = cmd.gas_name()
            index = calib.sensor_index(gas_name)

            if index is None:
                logger.error("%s is not included in the AFE calibration document." % gas_name)
                exit(1)

            baseline = AFEBaseline([baseline.sensor_baseline(index)])

        # zero...
        if cmd.zero:
            for index in range(len(baseline)):
                baseline.set_sensor_baseline(index, SensorBaseline(now, 0))

            baseline.save(Host)

        # delete...
        if cmd.delete:
            AFEBaseline.delete(Host)
            baseline = None

        # report...
        if baseline:
            print(JSONify.dumps(baseline))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        print(file=sys.stderr)

    finally:
        I2C.Sensors.close()
