#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The batt_pack_conf utility is used to specify whether a South Coast Science power supply (PSU) board is present
and if so, which model is provided. One model is currently available:

* V1

Note that the scs_dev/status_sampler process must be restarted for changes to take effect.

SYNOPSIS
batt_pack_conf.py [{ -m MODEL | -d }] [-v]

EXAMPLES
./batt_pack_conf.py -m V1

DOCUMENT EXAMPLE
{"model": "V1"}

FILES
~/SCS/conf/batt_pack_conf.json

SEE ALSO
scs_dev/psu
scs_dev/status_sampler
"""

import sys

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_batt_pack_conf import CmdBattPackConf

from scs_psu.batt_pack.batt_pack_conf import BattPackConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdBattPackConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("batt_pack_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # PSUConf...
    conf = BattPackConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        try:
            conf = BattPackConf(cmd.model)
            conf.save(Host)

        except ValueError as ex:
            print("batt_pack_conf: %s" % ex, file=sys.stderr)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
