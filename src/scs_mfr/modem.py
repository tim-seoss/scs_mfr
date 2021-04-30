#!/usr/bin/env python3

"""
Created on 20 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The modem utility is used to

SYNOPSIS
modem.py { -c | -s } [-v]

EXAMPLES
./modem.py -s

DOCUMENT EXAMPLE - CONNECTION
{"state": "connected", "signal": {"quality": 34, "recent": true}}

DOCUMENT EXAMPLE - SIM
{"imsi": "234104886708667", "iccid": "8944110068256270054", "operator-code": "23410", "operator-name": "O2 - UK"}

SEE ALSO
scs_mfr/configuration
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_modem import CmdModem


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    report = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdModem()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    Logging.config('modem', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.connection:
        report = Host.modem_connection()

    if cmd.sim:
        report = Host.sim()

    if report:
        print(JSONify.dumps(report))

