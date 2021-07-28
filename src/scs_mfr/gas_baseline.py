#!/usr/bin/env python3

"""
Created on 19 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The gas_baseline utility is used to adjust the zero offset for electrochemical sensors, as interpreted by the
current gas interpretation machine learning model.

If the system reports a concentration of 25 parts per billion in zero air, its zero offset should be set to -25.
The date / time of any change is recorded.

The environmental temperature, relative humidity and, optionally, absolute barometric pressure are stored alongside
the offset. These environmental parameters may be sourced either from sensors at the moment at which the offset is
recorded (the default), or supplied on the command line.

Each sensor is identified by the gas that it detects. For example, a nitrogen dioxide sensor is identified as NO2, and
an ozone sensor is identified as Ox.

Note that the scs_dev/gasses_sampler and greengrass processes must be restarted for changes to take effect.

SYNOPSIS
gas_baseline.py [{ { { -s | -o } GAS VALUE | -c GAS CORRECT REPORTED } [-r HUMID -t TEMP [-p PRESS]] | -z }] [-v]

EXAMPLES
./gas_baseline.py -c NO2 10 23

DOCUMENT EXAMPLE
{"CO": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 2, "env": {"hmd": 41.5, "tmp": 22.1, "pA": null}},
"NO2": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 1, "env": {"hmd": 41.5, "tmp": 22.1, "pA": null}}}

FILES
~/SCS/conf/gas_baseline.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/afe_calib
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.model.gas.gas_baseline import GasBaseline

from scs_core.gas.sensor_baseline import SensorBaseline, BaselineEnvironment

from scs_dfe.climate.pressure_conf import PressureConf
from scs_dfe.climate.sht_conf import SHTConf

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
        print("gas_baseline: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    try:
        I2C.Sensors.open()

        # ------------------------------------------------------------------------------------------------------------
        # resources...

        gas_baseline = GasBaseline.load(Host, skeleton=True)

        if not cmd.env_is_specified():
            # SHTConf...
            sht_conf = SHTConf.load(Host)

            if sht_conf is None:
                print("gas_baseline: SHTConf not available.", file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print("gas_baseline: %s" % sht_conf, file=sys.stderr)

            # SHT...
            sht = sht_conf.int_sht()

            # PressureConf...
            pressure_conf = PressureConf.load(Host)

            if pressure_conf is not None:
                if cmd.verbose:
                    print("gas_baseline: %s" % pressure_conf, file=sys.stderr)

                # barometer...
                barometer = pressure_conf.sensor(None)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        now = LocalizedDatetime.now().utc()

        if barometer is not None:
            barometer.init()

        # update...
        if cmd.update():
            old_offset = gas_baseline.sensor_offset(cmd.gas_name())

            if cmd.set:
                new_offset = cmd.set_value()

            elif cmd.offset:
                new_offset = old_offset + cmd.offset_value()

            else:
                new_offset = old_offset + (cmd.correct_value() - cmd.reported_value())

            if cmd.env_is_specified():
                humid = cmd.humid
                temp = cmd.temp
                press = cmd.press

            else:
                sht_datum = sht.sample()
                mpl_datum = None if barometer is None else barometer.sample()

                humid = sht_datum.humid
                temp = sht_datum.temp
                press = None if mpl_datum is None else mpl_datum.actual_press

            env = BaselineEnvironment(humid, temp, press)

            gas_baseline.set_sensor_baseline(cmd.gas_name(), SensorBaseline(now, new_offset, env))
            gas_baseline.save(Host)

            if cmd.verbose:
                print("gas_baseline: %s: was: %s now: %s" % (cmd.gas_name(), old_offset, new_offset), file=sys.stderr)

        # baseline...
        elif cmd.baseline:
            gas_name = cmd.gas_name()
            sensor_baseline = gas_baseline.sensor_baseline(gas_name)

            if sensor_baseline is None:
                print("gas_baseline: %s is not included in the calibration document." % gas_name, file=sys.stderr)
                exit(1)

            gas_baseline = GasBaseline({gas_name: sensor_baseline})

        # zero...
        elif cmd.zero:
            for gas in gas_baseline.gases():
                gas_baseline.set_sensor_baseline(gas, SensorBaseline(now, 0, None))

            gas_baseline.save(Host)

        # report...
        print(JSONify.dumps(gas_baseline))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("gas_baseline: KeyboardInterrupt", file=sys.stderr)

    finally:
        I2C.Sensors.close()
