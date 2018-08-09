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
dfe_conf.py [{ -s [-p ADDR] | -d }] [-v]

EXAMPLES
./dfe_conf.py -s

DOCUMENT EXAMPLE
{"pt1000-addr": 0x68}

FILES
~/SCS/conf/dfe_conf.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/pt1000_calib
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.board.dfe_conf import DFEConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_dfe_conf import CmdDFEConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdDFEConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("dfe_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # DFEConf...
    conf = DFEConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        conf = DFEConf(cmd.pt1000_addr)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
