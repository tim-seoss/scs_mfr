#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The psu_conf utility is used to specify whether a South Coast Science power supply (PSU) board is present
and if so, which model is provided. Three models are currently available:

* MobileV1 via PZHBt1 or PZHBt2 interface
* PrototypeV1 via serial port
* OsloV1 via serial port

Note that the scs_dev/psu_monitor process must be restarted for changes to take effect.

SYNOPSIS
psu_conf.py [{ -m MODEL [-f REPORT_FILE] | -d }] [-v]

EXAMPLES
./psu_conf.py -m OsloV1 -f /tmp/southcoastscience/psu_report.json

DOCUMENT EXAMPLE
{"model": "OsloV1", "report-file": "/tmp/southcoastscience/psu_status_report.json"}

FILES
~/SCS/conf/psu_conf.json

SEE ALSO
scs_dev/psu
scs_dev/psu_monitor
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
        model = cmd.model if cmd.model is not None else conf.model
        report_file = cmd.report_file if cmd.report_file is not None else conf.report_file

        try:
            conf = PSUConf(model, report_file)
            conf.save(Host)

        except ValueError as ex:
            print("psu_conf: %s" % ex, file=sys.stderr)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
