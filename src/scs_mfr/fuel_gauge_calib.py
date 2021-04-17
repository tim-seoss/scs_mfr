#!/usr/bin/env python3

"""
Created on 16 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The fuel_gauge_calib utility is used to interrogate or update the fuel gauge parameters on an attached battery pack.

Parameters are found automatically though a learning process run by the fuel gauge throughout its lifetime. These
values are saved to the file system by the PSU monitor every time the parameters change. The
battery pack model incorporates a set of parameter values gained through this process on test systems,
referred to as the default parameters.

When a new fuel gauge is put into use, it should be initialised with these values using the fuel_gauge_calib utility
--initialise flag - this sets both the parameters and the fuel gauge configuration.

SYNOPSIS
fuel_gauge_calib.py { { -c | -d | -l | -r | -z { D | L } } | { -f | -s | -g | -p } [-i INTERVAL] } [-v]

EXAMPLES
./batt_conf.py -i5 -f

DOCUMENT EXAMPLE - CONFIGURATION
{"des-cap": 3000, "sense-res": 0.01, "chrg-term": 10, "empty-v-target": 3.3, "recovery-v": 3.8, "chrg-v": 0,
"batt-type": 0}

DOCUMENT EXAMPLE - LEARNED PARAMS
{"calibrated-on": "2021-01-03T09:25:52Z", "r-comp-0": 255, "temp-co": 9278, "full-cap-rep": 3000, "full-cap-nom": 3000,
"cycles": 150}

DOCUMENT EXAMPLE - FUEL
{"in": false, "chrg": {"%": 1.0, "mah": 0}, "tte": null, "ttf": null, "v": 3.8, "curr": -486, "g-tmp": 25.5, "cap": 0,
"cyc": 2.0}

DOCUMENT EXAMPLE - PSU
{"src": "Cv1", "standby": false, "in": false, "pwr-in": 0.1, "chgr": "TFFT",
"batt": {"chg": 1, "tte": null, "ttf": null}, "prot-batt": 3.8}

FILES
~/SCS/conf/max17055_params.json

SEE ALSO
scs_dev/psu
scs_dev/psu_monitor
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sys.logging import Logging

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_fuel_gauge_calib import CmdFuelGaugeCalib

from scs_psu.batt_pack.fuel_gauge.max17055.max17055_params import Max17055Params
from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdFuelGaugeCalib()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('fuel_gauge_calib', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # InterfaceConf...
    interface_conf = InterfaceConf.load(Host)

    if interface_conf is None:
        logger.error('InterfaceConf not available.')
        exit(1)

    interface_model = interface_conf.model

    # PSUConf...
    psu_conf = PSUConf.load(Host)

    if psu_conf is None:
        logger.error('PSUConf not available.')
        exit(1)

    logger.info(psu_conf)

    psu = psu_conf.psu(Host, interface_model)
    batt_pack = psu.batt_pack

    if batt_pack is None:
        logger.error('No battery pack available.')
        exit(1)

    logger.info(batt_pack)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        # single shot...
        if cmd.gauge_conf:
            gauge_conf = batt_pack.gauge_conf()
            print(JSONify.dumps(gauge_conf))
            exit(0)

        if cmd.default_learned:
            params = batt_pack.default_params()
            print(JSONify.dumps(params))
            exit(0)

        if cmd.host_learned:
            params = Max17055Params.load(Host)
            if params:
                print(JSONify.dumps(params))
            exit(0)

        if cmd.remove_learned:
            Max17055Params.delete(Host)
            exit(0)

        if cmd.init is not None:
            if cmd.init == 'D':
                params = batt_pack.default_params()
                params.save(Host)

            params = batt_pack.initialise(Host, force_config=True)
            print(JSONify.dumps(params))
            exit(0)

        # iterable...
        timer = IntervalTimer(cmd.interval)

        while timer.true():
            if cmd.gauge_learned:
                params = batt_pack.read_learned_params()
                print(JSONify.dumps(params))

            if cmd.save_learned:
                saved_params = Max17055Params.load(Host)
                params = batt_pack.read_learned_params()

                if params != saved_params:
                    params.save(Host)
                    print(JSONify.dumps(params))

            if cmd.fuel:
                fuel = batt_pack.sample()
                print(JSONify.dumps(fuel))

            if cmd.psu:
                datum = psu.status()
                print(JSONify.dumps(datum))

            if not cmd.interval:
                break

    except KeyboardInterrupt:
        print(file=sys.stderr)
