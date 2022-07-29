#!/usr/bin/env python3

"""
Created on 9 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The pressure_conf utility is used to specify whether or not a digital barometer is present and, optionally,
the altitude of the device. This information is used to determine the pressure at sea level ("p0"). If the altitude is
not specified, then no p0 value is returned by the pressure_sampler and climate_sampler utilities.

If the MPL115A2 sensor is used, then determination of p0 requires the temperature sensor in the MPL115A2 digital
barometer to be calibrated. This is done using the mpl115a2_calib utility.

Forthcoming versions of the pressure_conf utility will support a "GPS" mode, in which altitude is found from a GPS
receiver.

The climate_sampler and pressure_sampler sampler processes must be restarted for changes to take effect.

SYNOPSIS
pressure_conf.py { [-m MODEL] [-a ALTITUDE] | -d } [-v]

EXAMPLES
./pressure_conf.py -m ICP -a 100

FILES
~/SCS/conf/pressure_conf.json

DOCUMENT EXAMPLE
{"model": "ICP", "altitude": 100}

SEE ALSO
scs_dev/climate_sampler
scs_dev/pressure_sampler
scs_mfr/mpl115a2_calib
"""

import sys

from scs_core.climate.pressure_conf import PressureConf
from scs_core.data.json import JSONify

from scs_host.sys.host import Host
from scs_core.sys.logging import Logging

from scs_mfr.cmd.cmd_pressure_conf import CmdPressureConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdPressureConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('pressure_conf', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # PressureConf...
    skeleton = cmd.set()                                # only get a skeleton is a set is happening
    conf = PressureConf.load(Host, skeleton=skeleton)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        model = conf.model if cmd.model is None else cmd.model
        altitude = conf.altitude if cmd.altitude is None else cmd.altitude

        if model is None:
            logger.error('a model must be specified.')
            exit(2)

        conf = PressureConf(model, altitude)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
