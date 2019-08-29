#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The psu_conf utility is used to specify whether a South Coast Science power supply (PSU) board is present
and if so, which model is provided. Two models are currently available:

* MobileV1 via PZHBt1 or PZHBt2 interface
* PrototypeV1 via serial port
* OsloV1 via serial port

Note that the scs_dev/status_sampler process must be restarted for changes to take effect.

SYNOPSIS
psu_conf.py [{ -m MODEL | -d }] [-v]

EXAMPLES
./psu_conf.py -m OsloV1

DOCUMENT EXAMPLE
{"model": "OsloV1"}

FILES
~/SCS/conf/psu_conf.json

SEE ALSO
scs_dev/psu
scs_dev/status_sampler
"""

import sys

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_psu_conf import CmdPSUConf

from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdPSUConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("psu_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # PSUConf...
    conf = PSUConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        conf = PSUConf(cmd.model)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
