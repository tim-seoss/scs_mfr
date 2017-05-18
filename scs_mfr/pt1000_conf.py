#!/usr/bin/env python3

"""
Created on 13 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"int": "0x44", "ext": "0x45"}

command line example:
./sht_conf.py -v -i 0x44 -e 0x45
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
