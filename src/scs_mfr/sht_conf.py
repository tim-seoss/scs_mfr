#!/usr/bin/env python3

"""
Created on 13 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

SHT
    Internal I2C addr or None
    External I2C addr or None

Part 1 of 3: Configuration:

    1: ./dfe_conf.py -v -s -p PT1000_ADDR
  > 2: ./sht_conf.py -v -i INT_ADDR -e EXT_ADDR
    3: ./ndir_conf.py -v -m MODEL -t AVERAGING_TALLY
    4: ./opc_conf.py -v -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 }
    5: ./psu_conf.py -v -m MODEL
    6: ./gps_conf.py -v -m MODEL
    7: ./schedule.py -v [{-s NAME INTERVAL COUNT | -c NAME }]

Creates or deletes SHTConf document.

document example:
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
    # cmd...

    cmd = CmdSHTConf()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SHTConf...
    conf = SHTConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # validate...

    if conf is None and cmd.set() and not cmd.is_complete():
        print("No configuration is stored. sht_conf must therefore set both I2C addresses:", file=sys.stderr)
        cmd.print_help(sys.stderr)
        exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            cmd.print_help(sys.stderr)
            exit(1)

        int_addr = cmd.int_addr if cmd.int_addr is not None else conf.int_addr
        ext_addr = cmd.ext_addr if cmd.ext_addr is not None else conf.ext_addr

        conf = SHTConf(int_addr, ext_addr)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
