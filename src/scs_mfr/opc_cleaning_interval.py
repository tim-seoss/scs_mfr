#!/usr/bin/env python3

"""
Created on 3 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The opc_cleaning_interval utility is used to

SYNOPSIS
opc_cleaning_interval.py [-s INTERVAL] [-v]

EXAMPLES
./opc_cleaning_interval.py -s 0

SEE ALSO
scs_dev/scs_cleaner
scs_dev/particulates_sampler
scs_mfr/opc_conf
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_opc_cleaning_interval import CmdOPCCleaningInterval


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOPCCleaningInterval()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("opc_cleaning_interval: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        I2C.open(Host.I2C_SENSORS)

        # OPCConf...
        conf = OPCConf.load(Host)

        if conf is None:
            print("opc_cleaning_interval: OPCConf not available.", file=sys.stderr)
            exit(1)

        # OPC...
        opc = conf.opc(Host)

        if cmd.verbose:
            print("opc_cleaning_interval: %s" % opc, file=sys.stderr)
            print("opc_cleaning_interval: %s" % opc.cleaning_interval, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if opc.cleaning_interval is None:
            exit(0)

        if cmd.set():
            opc.cleaning_interval = cmd.interval
            opc.reset()

        print(JSONify.dumps(opc.cleaning_interval))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    finally:
        I2C.close()
