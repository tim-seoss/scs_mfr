#!/usr/bin/env python3

"""
Created on 27 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The interface_conf utility is used to specify whether a South Coast Science sensor interface board is present on the
host system and, if so, which type it is.

Types are:

* DFE - uses the Alphasense analogue front-end board
* IEI - uses the South Coast Science integrated electrochem interface

The scs_dev sampler processes must be restarted for changes to take effect.

SYNOPSIS
interface_conf.py [{ -s SOURCE | -d }] [-v]

EXAMPLES
./interface_conf.py -s DFE

DOCUMENT EXAMPLE
{"model": "DFE"}

FILES
~/SCS/conf/interface_conf.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/pt1000_calib
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_interface_conf import CmdInterfaceConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdInterfaceConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("interface_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # DFEConf...
    conf = InterfaceConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        conf = InterfaceConf(cmd.model)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
