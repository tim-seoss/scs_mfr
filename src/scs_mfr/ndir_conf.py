#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

NDIR
    Model or None

Part 1 of 3: Configuration:

    1: ./dfe_conf.py -v -s -p PT1000_ADDR
    2: ./sht_conf.py -v -i INT_ADDR -e EXT_ADDR
  > 3: ./ndir_conf.py -v -m MODEL -t AVERAGING_TALLY
    4: ./opc_conf.py -v -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 }
    5: ./psu_conf.py -v -m MODEL
    6: ./gps_conf.py -v -m MODEL
    7: ./schedule.py -v [{-s NAME INTERVAL COUNT | -c NAME }]

Creates or deletes NDIRConf document.

document example:
{"model": "SPINDIRv1", "tally": 10}

command line example:
./ndir_conf.py -m SPINDIRv1 -t 1
"""

import sys

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_ndir_conf import CmdNDIRConf

from scs_ndir.gas.ndir_conf import NDIRConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # NDIRConf...
    conf = NDIRConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("No configuration is stored. ndir_conf must therefore set all fields:", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        model = cmd.model if cmd.model else conf.model
        tally = cmd.tally if cmd.tally else conf.tally

        conf = NDIRConf(model, tally)
        conf.save(Host)

    elif cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
