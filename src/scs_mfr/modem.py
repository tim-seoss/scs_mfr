#!/usr/bin/env python3

"""
Created on 30 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The modem utility is used to report on the modem connection status and SIM parameters. The reports provided by this
utility are included in the configuration utility report.

SYNOPSIS
modem.py { -m | -c | -s } [-v]

EXAMPLES
./modem.py -s

DOCUMENT EXAMPLE - MODEL
{"id": "3f07553c31ce11715037ac16c24ceddcfb6f7a0b", "imei": "867962041294151", "mfr": "QUALCOMM INCORPORATED",
"model": "QUECTEL Mobile Broadband Module", "rev": "EC21EFAR06A01M4G"}

DOCUMENT EXAMPLE - CONNECTION
{"state": "connected", "signal": {"quality": 34, "recent": true}}

DOCUMENT EXAMPLE - SIM
{"imsi": "234104886708567", "iccid": "8944110068257270054", "operator-code": "23410", "operator-name": "O2 - UK"}

SEE ALSO
scs_dev/status_sampler
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

    if cmd.model:
        report = Host.modem()

    if cmd.connection:
        report = Host.modem_conn()

    if cmd.sim:
        report = Host.sim()

    if report:
        print(JSONify.dumps(report))

