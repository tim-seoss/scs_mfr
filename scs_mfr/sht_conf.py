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

from scs_dfe.climate.sht_conf import SHTConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_sht_conf import CmdSHTConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SHTConf...
    conf = SHTConf.load_from_host(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSHTConf()

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

        int_addr = cmd.int_addr if cmd.int_addr else conf.int_addr
        ext_addr = cmd.ext_addr if cmd.ext_addr else conf.ext_addr

        conf = SHTConf(int_addr, ext_addr)

        conf.save(Host)

    if conf:
        print(JSONify.dumps(conf))
