#!/usr/bin/env python3

"""
Created on 4 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The fuel_gauge_calib utility is used to interrogate or update the fuel gauge parameters on an attached battery pack.

Parameters are found automatically though a learning process run by the fuel gauge throughout its lifetime. These
values are saved to the file system by the PSU monitor every time the parameters change. The
battery pack model incorporates a set of parameter values gained through this process on test systems,
referred to as the default parameters.

When a new fuel gauge is put into use, it should be initialised with these values using the fuel_gauge_calib utility
--initialise flag - this sets both the parameters and the fuel gauge configuration. If a max17055_params.json
configuration file has been stored for this system, then it is used to initialise the parameters. Otherwise, the
default parameters for the configured battery pack are used.

SYNOPSIS
fuel_gauge_calib.py { { -n | -l { D | F } | -s } | { -c | -f | -p } [-i INTERVAL] } [-v]

EXAMPLES
./fuel_gauge_calib.py -cv

FILES
~/SCS/conf/max17055_params.json

DOCUMENT EXAMPLE - PARAMETERS
{"calibrated-on": "2021-01-02T09:34:48Z",
"r-comp-0": 201, "temp-co": 9278, "full-cap-rep": 1790, "full-cap-nom": 4896, "cycles": 210}

DOCUMENT EXAMPLE - FUEL
{"in": true, "chrg": {"%": 99.0, "mah": 1729}, "tte": null, "ttf": "00-02:55:24", "v": 4.1, "curr": 182,
"g-tmp": 30.7, "cap": 1729, "cyc": 2.9}

DOCUMENT EXAMPLE - PSU
{"src": "Cv1", "standby": false, "in": true, "pwr-in": 11.6, "chgr": "TFTF",
"batt": {"chg": 99, "tte": null, "ttf": "00-02:54:56"}, "prot-batt": 4.1}

SEE ALSO
scs_dev/psu_monitor
scs_mfr/psu_conf
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sync.interval_timer import IntervalTimer

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_fuel_gauge_calib import CmdFuelGaugeCalib

from scs_psu.batt_pack.fuel_gauge.max17055.max17055_params import MAX17055Params
from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    params = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdFuelGaugeCalib()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("fuel_gauge_calib: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        I2C.Sensors.open()

        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # Interface...
        interface_conf = InterfaceConf.load(Host)

        # PSU...
        psu_conf = PSUConf.load(Host)
        psu = psu_conf.psu(Host, interface_conf.model)

        if cmd.verbose:
            print("fuel_gauge_calib: %s" % psu, file=sys.stderr)

        batt_pack = psu.batt_pack

        if batt_pack is None:
            print("fuel_gauge_calib: PSU has no battery pack.", file=sys.stderr)
            exit(1)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # no auto-initialisation - we want to see the MAX17055 native values

        # single shot...
        if cmd.initialise:
            params = batt_pack.initialise(Host, force_config=True)
            params.save(Host)

        elif cmd.load == 'D':
            params = batt_pack.default_params()
            batt_pack.write_params(params)
            params.save(Host)

        elif cmd.load == 'F':
            params = MAX17055Params.load(Host)
            batt_pack.write_params(params)
            params.save(Host)

        elif cmd.save:
            params = batt_pack.read_learned_params()
            params.save(Host)

        if cmd.initialise or cmd.load or cmd.save:
            print(JSONify.dumps(params))
            exit(0)

        # iterable...
        timer = IntervalTimer(cmd.interval)

        while timer.true():
            if cmd.current:
                params = batt_pack.read_learned_params()
                print(JSONify.dumps(params))

            elif cmd.fuel:
                datum = batt_pack.sample()
                print(JSONify.dumps(datum))

            elif cmd.power:
                datum = psu.status()
                print(JSONify.dumps(datum))

            if not cmd.interval:
                break


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        print(file=sys.stderr)

    finally:
        I2C.Sensors.close()
