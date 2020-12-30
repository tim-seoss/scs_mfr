#!/usr/bin/env python3

"""
Created on 1 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The pt1000_calib utility is used to determine and save the voltage offset for each Pt1000 sensor.

The utility operates by measuring the temperature using a Sensirion SHT sensor, measuring the voltage output of the
Pt1000 sensor, and back-calculating the voltage offset.

For the utility to operate, the I2C address of the Pt1000 ADC must be set. This is done using the dfe_conf utility.

Note that the scs_analysis/gases_sampler process must be restarted for changes to take effect.

SYNOPSIS
pt1000_calib.py [{ -s | -d }] [-v]

EXAMPLES
./pt1000_calib.py -s

DOCUMENT EXAMPLE
{"calibrated-on": "2017-07-19T13:56:48.289+00:00", "v20": 0.002891}

FILES
~/SCS/conf/pt1000_calib.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/interface_conf
"""

import sys

from scs_core.data.json import JSONify

from scs_core.gas.afe.pt1000_calib import Pt1000Calib

from scs_dfe.interface.interface_conf import InterfaceConf
from scs_dfe.climate.sht_conf import SHTConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_pt1000_calib import CmdPt1000Calib


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.Sensors.open()

        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdPt1000Calib()

        if not cmd.is_valid():
            cmd.print_help(sys.stderr)
            exit(2)

        if cmd.verbose:
            print("pt1000_calib: %s" % cmd, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # Interface...
        interface_conf = InterfaceConf.load(Host)

        if interface_conf is None:
            print("pt1000_calib: InterfaceConf not available.", file=sys.stderr)
            exit(1)

        interface = interface_conf.interface()

        if interface is None:
            print("pt1000_calib: Interface not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose and interface:
            print("pt1000_calib: %s" % interface, file=sys.stderr)

        # SHT...
        sht_conf = SHTConf.load(Host)
        sht = sht_conf.int_sht()

        # validate...
        if interface.pt1000 is None:
            print("pt1000_calib: a Pt1000 ADC has not been configured for this system.", file=sys.stderr)
            exit(1)

        afe = interface.gas_sensors(Host)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.set:
            # SHT...
            sht_datum = sht.sample()

            if cmd.verbose:
                print(sht_datum, file=sys.stderr)

            # Pt1000 initial...
            pt1000_datum = afe.sample_pt1000()

            # Pt1000 correction...
            v20 = pt1000_datum.v20(sht_datum.temp)

            pt1000_calib = Pt1000Calib(None, v20)
            pt1000_calib.save(Host)

        elif cmd.delete:
            Pt1000Calib.delete(Host)
            pt1000_calib = None

        else:
            # load...
            pt1000_calib = Pt1000Calib.load(Host)

        # report...
        if pt1000_calib:
            print(JSONify.dumps(pt1000_calib))

        if cmd.verbose:
            afe = interface.gas_sensors(Host)
            pt1000_datum = afe.sample_pt1000()

            print(pt1000_datum, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    finally:
        I2C.Sensors.close()
