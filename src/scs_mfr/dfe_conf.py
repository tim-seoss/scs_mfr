#!/usr/bin/env python3

"""
Created on 27 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)


Part 1 of 3: Configuration:

  > 1: ./dfe_conf.py -v -s -p PT1000_ADDR
    2: ./sht_conf.py -v -i INT_ADDR -e EXT_ADDR
    3: ./ndir_conf.py -v -m MODEL -a AVERAGING_PERIOD
    4: ./opc_conf.py -v -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 }
    5: ./psu_conf.py -v -m MODEL
    6: ./gps_conf.py -v -m MODEL
    7: ./schedule.py -v [{-s NAME INTERVAL COUNT | -c NAME }]

Creates or deletes DFEConf document.

document example:
{"pt1000-addr": "0x69"}

command line example:
./dfe_conf.py -v -p 0x69
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
        print(cmd, file=sys.stderr)
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

    elif cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
