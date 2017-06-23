#!/usr/bin/env python3

"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

configuration workflow:
  > 1: ./pt1000_conf.py -a ADDR -v
    2: ./sht_conf.py -i INT_ADDR -e EXT_ADDR -v
    3: ./ndir_conf.py -p { 1 | 0 } -v

Creates Pt1000Conf document.

document example:
{"addr": "0x69"}

command line example:
./pt1000_conf.py -a 0x69 -v
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.gas.pt1000_conf import Pt1000Conf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_pt1000_conf import CmdPt1000Conf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # Pt1000Conf...
    conf = Pt1000Conf.load_from_host(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdPt1000Conf()

    if not cmd.is_valid(conf):
        cmd.print_help(sys.stderr)
        exit()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            cmd.print_help(sys.stderr)
            exit()

        conf = Pt1000Conf(cmd.addr)
        conf.save(Host)

    if conf:
        print(JSONify.dumps(conf))
