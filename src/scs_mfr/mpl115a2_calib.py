#!/usr/bin/env python3

"""
Created on 20 Jun 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The mpl115a2_calib utility is used to calibrate the temperature sensor in the MPL115A2 digital barometer. The utility
operates by measuring the temperature using a Sensirion SHT sensor, measuring the temperature ADC count of the MPL115A2
sensor, and back-calculating the offset.

If calibration has been performed, the pressure_sampler utility reports temperature in addition to actual pressure
("pA"). If the host device altitude has also been set, the pressure_sampler additionally reports equivalent pressure
at sea level ("p0").

The pressure_sampler sampler processes must be restarted for changes to take effect.

SYNOPSIS
mpl115a2_calib.py [{ -s | -d }] [-v]

EXAMPLES
./mpl115a2_calib.py -s

FILES
~/SCS/conf/mpl115a2_calib.json

DOCUMENT EXAMPLE
{"calibrated-on": "2018-06-20T10:25:39.045+00:00", "c25": 511}

SEE ALSO
scs_dev/pressure_sampler
scs_mfr/pressure_conf
"""

import sys

from scs_core.climate.mpl115a2_calib import MPL115A2Calib
from scs_core.climate.pressure_conf import PressureConf

from scs_core.data.json import JSONify

from scs_dfe.climate.mpl115a2 import MPL115A2
from scs_dfe.climate.sht_conf import SHTConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_mpl115a2_calib import CmdMPL115A2Calib


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    sht_datum = None

    try:
        I2C.Sensors.open()

        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdMPL115A2Calib()

        if not cmd.is_valid():
            cmd.print_help(sys.stderr)
            exit(2)

        if cmd.verbose:
            print("mpl115a2_calib: %s" % cmd, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # PressureConf...
        conf = PressureConf.load(Host)

        if conf is None:
            print("mpl115a2_calib: PressureConf not available.", file=sys.stderr)
            exit(1)

        # SHT...
        sht_conf = SHTConf.load(Host)

        if sht_conf is None:
            print("mpl115a2_calib: SHTConf not available.", file=sys.stderr)
            exit(1)

        sht = sht_conf.int_sht()

        # MPL115A2Calib...
        calib = MPL115A2Calib.load(Host)

        c25 = MPL115A2Calib.DEFAULT_C25 if calib is None else calib.c25

        # MPL115A2...
        barometer = MPL115A2(c25)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        barometer.init()

        if cmd.set:
            # SHT...
            try:
                sht_datum = sht.sample()
            except OSError:
                print("mpl115a2_calib: SHT31 not available", file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print(sht_datum, file=sys.stderr)

            # MPL115A2 initial...
            datum = barometer.sample()

            # MPL115A2 correction...
            c25 = datum.c25(sht_datum.temp)

            calib = MPL115A2Calib(None, c25)
            calib.save(Host)

            # calibrated...
            calib = MPL115A2Calib.load(Host)

        elif cmd.delete and calib is not None:
            calib.delete(Host)
            calib = None

        if calib:
            print(JSONify.dumps(calib))

        if cmd.verbose:
            barometer = MPL115A2.construct(calib)
            barometer.init()

            datum = barometer.sample()

            print(datum, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except OSError:
        print("mpl115a2_calib: MPL115A2 not available", file=sys.stderr)

    finally:
        I2C.Sensors.close()
