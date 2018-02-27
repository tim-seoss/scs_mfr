#!/usr/bin/env python3

"""
Created on 27 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)


Part 1 of 3: Configuration:

  > 1: ./dfe_conf.py -v -p 0x69
    2: ./sht_conf.py -i INT_ADDR -e EXT_ADDR -v
    3: ./opc_conf.py -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 } -v
    4: ./psu_conf.py -m { PrototypeV1 | OsloV1 } -v
    5: ./ndir_conf.py -p { 1 | 0 } -v
    6: ./gps_conf.py -m MODEL -v
    7: ./schedule.py [{-s NAME INTERVAL COUNT | -c NAME }] [-v]

Creates DFEConf document.

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

    if cmd.set:
        conf = DFEConf(cmd.pt1000_addr)
        conf.save(Host)

    elif cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
