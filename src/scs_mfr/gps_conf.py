#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The gps_conf utility is used to specify whether a GPS receiver module is present and if so, which model is provided.

Currently, only the u-blox PAM7Q module is supported.

SYNOPSIS
gps_conf.py [{ -m MODEL | -d }] [-v]

EXAMPLES
./gps_conf.py -m PAM7Q

DOCUMENT EXAMPLE
{"model": "PAM7Q"}

FILES
~/SCS/conf/gps_conf.json

SEE ALSO
scs_dev/status_sampler
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.gps.gps_conf import GPSConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_gps_conf import CmdGPSConf


# TODO: add stationery / mobile mode (averaging count)

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # GPSConf...
    conf = GPSConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdGPSConf()

    if cmd.verbose:
        print("gps_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        conf = GPSConf(cmd.model, GPSConf.DEFAULT_SAMPLE_INTERVAL, GPSConf.DEFAULT_TALLY)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
