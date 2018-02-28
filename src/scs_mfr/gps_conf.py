#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

GPS
    Model or None

Part 1 of 3: Configuration:

    1: ./dfe_conf.py -v -s -p PT1000_ADDR
    2: ./sht_conf.py -v -i INT_ADDR -e EXT_ADDR
    3: ./ndir_conf.py -v -m MODEL -t AVERAGING_TALLY
    4: ./opc_conf.py -v -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 }
    5: ./psu_conf.py -v -m MODEL
  > 6: ./gps_conf.py -v -m MODEL
    7: ./schedule.py -v [{-s NAME INTERVAL COUNT | -c NAME }]

Creates or deletes GPSConf document.

document example:
{"model": "PAM7Q"}

command line example:
./gps_conf.py -m PAM7Q -v
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.gps.gps_conf import GPSConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_gps_conf import CmdGPSConf


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
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        conf = GPSConf(cmd.model)
        conf.save(Host)

    elif cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
