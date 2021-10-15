#!/usr/bin/env python3

"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The vcal_baseline utility is used to adjust the zero offset of the reported vCal value.

IMPORTANT NOTE: the vCal baseline does not change the vCal value as reported by the gases_sampler utility. Instead,
it is used by the gas exegesis system, as part of the preprocessing of data that is passed to the interpretation
model.

Each sensor is identified by the gas that it detects. For example, a nitrogen dioxide sensor is identified as NO2, and
an ozone sensor is identified as Ox.

Note that the greengrass processes must be restarted for changes to take effect.

SYNOPSIS
vcal_baseline.py [{ { -b GAS  | { -s | -o } GAS VALUE | -c GAS CORRECT REPORTED } \
[-r HUMID -t TEMP [-p PRESS]] | -z }] [-v]

EXAMPLES
./vcal_baseline.py -c NO2 -16 -65

DOCUMENT EXAMPLE
{"CO": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 2, "env": {"hmd": 41.5, "tmp": 22.1, "pA": null}},
"NO2": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 1, "env": {"hmd": 41.5, "tmp": 22.1, "pA": null}}}

FILES
~/SCS/conf/vcal_baseline.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/afe_calib
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.model.gas.vcal_baseline import VCalBaseline

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
        print("vcal_baseline: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    try:
        I2C.Sensors.open()

        # ------------------------------------------------------------------------------------------------------------
        # resources...

        vcal_baseline = VCalBaseline.load(Host, skeleton=True)

        if not cmd.env_is_specified():
            # SHTConf...
            sht_conf = SHTConf.load(Host)

            if sht_conf is None:
                print("vcal_baseline: SHTConf not available.", file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print("vcal_baseline: %s" % sht_conf, file=sys.stderr)

            # SHT...
            sht = sht_conf.int_sht()

            # PressureConf...
            pressure_conf = PressureConf.load(Host)

            if pressure_conf is not None:
                if cmd.verbose:
                    print("vcal_baseline: %s" % pressure_conf, file=sys.stderr)

                # barometer...
                barometer = pressure_conf.sensor(None)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        now = LocalizedDatetime.now().utc()

        if barometer is not None:
            barometer.init()

        # update...
        if cmd.update():
            old_offset = vcal_baseline.sensor_offset(cmd.gas_name())

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

            vcal_baseline.set_sensor_baseline(cmd.gas_name(), SensorBaseline(now, new_offset, env))
            vcal_baseline.save(Host)

            if cmd.verbose:
                print("vcal_baseline: %s: was: %s now: %s" % (cmd.gas_name(), old_offset, new_offset), file=sys.stderr)

        # baseline...
        elif cmd.baseline:
            gas_name = cmd.gas_name()
            sensor_baseline = vcal_baseline.sensor_baseline(gas_name)

            if sensor_baseline is None:
                print("vcal_baseline: %s is not included in the calibration document." % gas_name, file=sys.stderr)
                exit(1)

            vcal_baseline = VCalBaseline({gas_name: sensor_baseline})

        # zero...
        elif cmd.zero:
            for gas in vcal_baseline.gases():
                vcal_baseline.set_sensor_baseline(gas, SensorBaseline(now, 0, None))

            vcal_baseline.save(Host)

        # report...
        print(JSONify.dumps(vcal_baseline))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print(file=sys.stderr)

    finally:
        I2C.Sensors.close()
