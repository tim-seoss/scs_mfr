#!/usr/bin/env python3

"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

OPC
    Model or None
    Sample period
    Power saving

Part 1 of 3: Configuration:

    1: ./dfe_conf.py -v -s -p PT1000_ADDR
    2: ./sht_conf.py -v -i INT_ADDR -e EXT_ADDR
    3: ./ndir_conf.py -v -m MODEL -t AVERAGING_TALLY
  > 4: ./opc_conf.py -v -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 }
    5: ./psu_conf.py -v -m MODEL
    6: ./gps_conf.py -v -m MODEL
    7: ./schedule.py -v [{-s NAME INTERVAL COUNT | -c NAME }]

Creates or deletes OPCConf document.

document example:
{"model": "N2", "sample-period": 10, "power-saving": false}

command line example:
./opc_conf.py -m N2 -s 10 -p 0 -v
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_opc_conf import CmdOPCConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOPCConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # OPCConf...
    conf = OPCConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("opc_conf: No configuration is stored. You must therefore set all fields.", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        model = cmd.model if cmd.model else conf.model
        sample_period = cmd.sample_period if cmd.sample_period else conf.sample_period
        power_saving = cmd.power_saving if cmd.power_saving is not None else conf.power_saving

        conf = OPCConf(model, sample_period, power_saving)
        conf.save(Host)

    elif cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
