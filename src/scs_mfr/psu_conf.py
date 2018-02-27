#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

PSU
    Model or None

Part 1 of 3: Configuration:

    1: ./dfe_conf.py -v -s -p PT1000_ADDR
    2: ./sht_conf.py -v -i INT_ADDR -e EXT_ADDR
    3: ./ndir_conf.py -v -m MODEL
    4: ./opc_conf.py -v -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 }
  > 5: ./psu_conf.py -v -m MODEL
    6: ./gps_conf.py -v -m MODEL
    7: ./schedule.py -v [{-s NAME INTERVAL COUNT | -c NAME }]

Creates or deletes PSUConf document.

document example:
{"model": "PrototypeV1"}

command line example:
./psu_conf.py -m OsloV -v
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
        print(cmd, file=sys.stderr)
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

    elif cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
