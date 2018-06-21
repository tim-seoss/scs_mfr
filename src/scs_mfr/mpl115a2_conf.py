#!/usr/bin/env python3

"""
Created on 27 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The dfe_conf utility is used to specify whether a South Coast Science digital front-end (DFE) board is present on the
host system, and whether the attachAlphasense analogue front-end board has a Pt1000 sensor.

Pt1000 analogue-digital converter (ADC) I2C addresses:

* Raspberry Pi DFE: 0x68
* BeagleBone DFE: 0x69

Note: many device enclosure designs cause the Pt1000 reading to be unreliable. In these cases, it is appropriate
to specify that the Pt1000 is absent.

The scs_dev sampler processes must be restarted for changes to take effect.

SYNOPSIS
mpl115a2_conf.py [{ -s [-a ALTITUDE] | -d }] [-v]

EXAMPLES
./mpl115a2_conf.py -s

DOCUMENT EXAMPLE
{"altitude": "auto"}

FILES
~/SCS/conf/dfe_conf.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/mpl115a2_calib
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.climate.mpl115a2_conf import MPL115A2Conf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_mpl115a2_conf import CmdMPL115A2Conf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdMPL115A2Conf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("mpl115a2_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # DFEConf...
    conf = MPL115A2Conf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        conf = MPL115A2Conf(cmd.altitude)
        conf.save(Host)

    elif cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
